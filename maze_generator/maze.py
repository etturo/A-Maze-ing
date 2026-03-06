from maze_generator.settings_reader import MazeSettings
from maze_generator.cell import Cell, Direction
from typing import List


class Maze:
    def __init__(self, settings: MazeSettings):
        self.__settings: MazeSettings = settings
        self.__map: List[list[Cell]] = []
        self.__solution: List[Direction] = []

        for height in range(int(self.__settings['HEIGHT'])):
            row: List[Cell] = list()
            for width in range(int(self.__settings['WIDTH'])):
                row.append(Cell(15))
            self.__map.append(row)

    def __str__(self):
        return self.serialize()

    def serialize(self) -> None:
        with open(self.__settings['OUTPUT_FILE'], 'w') as file:
            for line in self.__map:
                for row in line:
                    file.write(hex(row.walls)[2:])
                file.write("\n")

            file.write('\n' + self.__settings['ENTRY'])
            file.write('\n' + self.__settings['EXIT'] + '\n')

            for direction in self.__solution:
                file.write(str(direction))
