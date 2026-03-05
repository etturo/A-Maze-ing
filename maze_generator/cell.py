from enum import IntEnum


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class Cell:
    def __init__(self) -> None:
        self.walls: int = 0

    def HasWall(self, dir: Direction) -> bool:
        return (self.walls & dir) != 0

    def __setitem__(self, d: Direction, value: bool):
        self.walls = (self.walls | d) if value else (self.walls & (15 & ~d))
