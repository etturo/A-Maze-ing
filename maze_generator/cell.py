from enum import IntEnum
from typing import Dict


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __str__(self):
        return self.name[0]


class Cell:
    full_cell: str = "██"
    empty_cell: str = "  "

    def __init__(self, full: bool) -> None:
        self.full = full

    def SetNeighbors(self, neighbors: Dict[Direction, "Cell"]):
        self.__neighbors = neighbors

    def IsFull(self):
        return self.full

    def __str__(self) -> str:
        n: Dict[Direction, "Cell"] = self.__neighbors
        return hex(n[Direction.NORTH].IsFull() * Direction.NORTH +
                   n[Direction.EAST].IsFull() * Direction.EAST +
                   n[Direction.SOUTH].IsFull() * Direction.SOUTH +
                   n[Direction.WEST].IsFull() * Direction.WEST)

    def get_sprite(self) -> str:
        return (Cell.full_cell if self.full else Cell.empty_cell)
