from enum import IntEnum


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __str__(self):
        return self.name[0]


class Cell:
    def __init__(self, wall: int) -> None:
        self.walls: int = wall

    def HasWall(self, dir: Direction) -> bool:
        return (self.walls & dir) != 0

    def __setitem__(self, d: Direction, value: bool):
        self.walls = (self.walls | d) if value else (self.walls & ~d)
