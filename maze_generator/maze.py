from maze_generator.settings_reader import MazeSettings
from maze_generator.cell import Cell, Direction
from typing import List


class MazeRender:
    def __init__(self, maze: "Maze") -> None:
        self.__render_width = maze.width*2+1
        self.__render_height = maze.height*2+1
        self.maze = maze
        self.render: list[list[str]] = list()

        for y in range(self.__render_height):
            row: list[list[str]] = list()
            for x in range(self.__render_width):
                row.append(" ")
            self.render.append(row)

    def __get_neighbor(self, x: int, y: int) -> int:
        result: int = 0
        result |= Direction.NORTH if y > 0 and self.render[y-1][x] != " " else 0
        result |= Direction.EAST if x < self.__render_width-1 and self.render[y][x+1] != " " else 0
        result |= Direction.SOUTH if y < self.__render_height-1 and self.render[y+1][x] != " " else 0
        result |= Direction.WEST if x > 0 and self.render[y][x-1] != " " else 0
        return result

    def Render(self) -> str:
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rx: int = x * 2 + 1
                ry: int = y * 2 + 1
                self.render[ry][rx] = "."
                self.render[ry-1][rx] = self.maze.GetCell(x, y).GetWallSprite(Direction.NORTH)
                self.render[ry][rx-1] = self.maze.GetCell(x, y).GetWallSprite(Direction.WEST)
                self.render[ry][rx+1] = self.maze.GetCell(x, y).GetWallSprite(Direction.EAST)
                self.render[ry+1][rx] = self.maze.GetCell(x, y).GetWallSprite(Direction.SOUTH)

        for y in range(1, self.__render_height, 2):
            for x in range(1, self.__render_width, 2):
                self.render[y-1][x-1] = str(self.__get_neighbor(x-1,y-1))
                self.render[y-1][x+1] = str(self.__get_neighbor(x+1,y-1))
                self.render[y+1][x-1] = str(self.__get_neighbor(x-1,y+1))
                self.render[y+1][x+1] = str(self.__get_neighbor(x+1,y+1))

        return "\n".join("".join(row) for row in self.render)


class Maze:
    def __getBorder(self, x: int, y: int) -> int:
        wall_border: int = 0x0
        if (x == 0):
            wall_border = Cell.AddWall(wall_border, Direction.WEST)
        if (y == 0):
            wall_border = Cell.AddWall(wall_border, Direction.NORTH)
        if (x == self.width - 1):
            wall_border = Cell.AddWall(wall_border, Direction.EAST)
        if (y == self.height - 1):
            wall_border = Cell.AddWall(wall_border, Direction.SOUTH)
        return wall_border

    def __init__(self, settings: MazeSettings):
        self.__settings: MazeSettings = settings
        self.__map: List[list[Cell]] = []
        self.width: int = int(self.__settings['WIDTH'])
        self.height: int = int(self.__settings['HEIGHT'])
        self.__solution: List[Direction] = []
        self.render = MazeRender(self)

        for y in range(self.height):
            row: List[Cell] = list()
            for x in range(self.width):
                row.append(Cell(settings.wall_graphics,
                                walls=0x0,
                                invicible_walls=self.__getBorder(x, y),))
            self.__map.append(row)

    def __str__(self) -> str:
        return self.render.Render()

    def Serialize(self) -> None:
        with open(self.__settings['OUTPUT_FILE'], 'w') as file:
            for line in self.__map:
                for cell in line:
                    file.write(cell.Serialize()[2:])
                file.write("\n")

            file.write('\n' + self.__settings['ENTRY'])
            file.write('\n' + self.__settings['EXIT'] + '\n')

            for direction in self.__solution:
                file.write(str(direction))

    def GetCell(self, x: int, y: int) -> Cell:
        return self.__map[y][x]
