from maze_generator.settings_reader import MazeSettings
from maze_generator.cell import Cell, Direction
from typing import List


class Maze:
    def __init__(self, settings: MazeSettings):
        self.__settings: MazeSettings = settings
        self.__map: List[list[Cell]] = []
        self.__solution: List[Direction] = []

        width: int = int(self.__settings['WIDTH'])
        height: int = int(self.__settings['HEIGHT'])

        for y in range(height):
            row: List[Cell] = list()
            for x in range(width):
                row.append(Cell(False))
            self.__map.append(row)

        for y in range(height):
            for x in range(width):
                self.__map[y][x].SetNeighbors({
                    Direction.NORTH: self.__map[y-1][x] if y > 0 else
                    Cell(True),
                    Direction.EAST: self.__map[y][x+1] if x < width-1 else
                    Cell(True),
                    Direction.SOUTH: self.__map[y+1][x] if y < height-1 else
                    Cell(True),
                    Direction.WEST: self.__map[y][x-1] if x > 0 else
                    Cell(True)
                })

    def __str__(self):
        return self.serialize()

    def serialize(self) -> None:
        with open(self.__settings['OUTPUT_FILE'], 'w') as file:
            for line in self.__map:
                for cell in line:
                    file.write(str(cell)[2:])
                file.write("\n")

            file.write('\n' + self.__settings['ENTRY'])
            file.write('\n' + self.__settings['EXIT'] + '\n')

            for direction in self.__solution:
                file.write(str(direction))
