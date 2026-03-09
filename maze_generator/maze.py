from maze_generator.settings_reader import MazeSettings, WallGraphics
from maze_generator.cell import Cell, Direction, ReadonlyCell
from typing import List


class MazeRender:
    def __init__(self, maze: "Maze", settings: WallGraphics) -> None:
        self.__maze = maze
        self.__settings = settings
        self.__w = maze.width * 2 + 1
        self.__h = maze.height * 2 + 1

        self.__render = [[False] * self.__w for _ in range(self.__h)]

    def __check_wall(self, x: int, y: int) -> bool:
        return (x >= 0 and x < self.__w and
                y >= 0 and y < self.__h and
                self.__render[y][x])

    def __get_neighbor(self, x: int, y: int) -> int:
        if not self.__render[y][x]:
            return 0
        result: int = 0

        result |= Direction.NORTH if self.__check_wall(x, y-1) else 0
        result |= Direction.EAST if self.__check_wall(x+1, y) else 0
        result |= Direction.SOUTH if self.__check_wall(x, y+1) else 0
        result |= Direction.WEST if self.__check_wall(x-1, y) else 0
        return result

    def Render(self) -> str:
        result: str = ""
        for y in range(self.__maze.height):
            for x in range(self.__maze.width):
                rx: int = x * 2 + 1
                ry: int = y * 2 + 1
                cell: ReadonlyCell = self.__maze[x, y]
                n = cell.HasWall(Direction.NORTH)
                w = cell.HasWall(Direction.WEST)
                e = cell.HasWall(Direction.EAST)
                s = cell.HasWall(Direction.SOUTH)

                self.__render[ry-1][rx] |= n
                self.__render[ry][rx-1] |= w
                self.__render[ry][rx+1] |= e
                self.__render[ry+1][rx] |= s

                self.__render[ry-1][rx-1] |= n or w
                self.__render[ry-1][rx+1] |= n or e
                self.__render[ry+1][rx-1] |= s or w
                self.__render[ry+1][rx+1] |= s or e

        s = self.__settings
        for y in range(self.__h):
            for x in range(self.__w):
                char = s[self.__get_neighbor(x, y)]
                # Doubles Every odd indexed character to fix vertical stretch
                result += char * (2 if x % 2 == 1 else 1)
            result += "\n"

        return result


class Maze:
    def __getBorder(self, x: int, y: int) -> int:
        return ((Direction.WEST if x == 0 else 0) |
                (Direction.NORTH if y == 0 else 0) |
                (Direction.EAST if x == self.width - 1 else 0) |
                (Direction.SOUTH if y == self.height - 1 else 0))

    def __init__(self, settings: MazeSettings):
        self.__settings: MazeSettings = settings
        self.__map: List[list[Cell]] = []
        self.width: int = int(self.__settings['WIDTH'])
        self.height: int = int(self.__settings['HEIGHT'])
        self.__solution: List[Direction] = []
        self.render = MazeRender(self, settings.wall_graphics)

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

    def __getitem__(self, pos: tuple[int, int]) -> ReadonlyCell:
        x, y = pos
        return ReadonlyCell(self.__map[y][x])

    def AddWall(self, x: int, y: int, wall: Direction) -> None:
        self.__map[y][x] += wall
        self.__map[y+wall.vector[1]][x+wall.vector[0]] += wall.opposite
