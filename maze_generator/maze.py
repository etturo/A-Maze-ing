from cell import Cell
from settings_reader import MazeSettings


class Maze:
    def __init__(self, settings: MazeSettings):
        self.__settings: MazeSettings = settings
        self.__map: list[list[Cell]] = [
            [Cell() for _ in range(int(settings["WIDTH"]))]
            for _ in range(int(settings["HEIGHT"]))]
