from maze_generator.settings_reader import MazeSettings
from maze_generator.cell import Cell
from typing import List


class Maze:
    def __init__(self, settings: MazeSettings):
        self.__settings: MazeSettings = settings
        self.__map: list[list[Cell]] = []

        for height in range(int(self.__settings['HEIGHT'])):
            row: List[Cell] = list()
            for width in range(int(self.__settings['WIDTH'])):
                row.append(Cell(15))
            self.__map.append(row)

    def __str__(self):
        return self.serialize()

    def serialize(self) -> str:
        maze_str: str = ""

        for line in self.__map:
            for row in line:
                maze_str += hex(row.walls)[2:]
            maze_str += "\n"

        return maze_str
