from maze_generator.settings_reader import MazeSettings
from maze_generator.cell import Cell, Direction
from typing import List


class Maze:
    # not sure if this is the correct place for this
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

        for y in range(self.height):
            row: List[Cell] = list()
            for x in range(self.width):
                row.append(Cell(settings.wall_graphics,
                                walls=0x0,
                                invicible_walls=self.__getBorder(x, y),))
            self.__map.append(row)

# each cell should draw the 9 walls around her (if they were not draw before
# only drawing top and left walls for each cell doesnt work in this case
    def __str__(self) -> str:
        result: str = str()
        return result

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
