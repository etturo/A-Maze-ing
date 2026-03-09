from enum import IntEnum
from maze_generator.settings_reader import WallGraphics


class InvalidCellOperation(Exception):
    pass


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __str__(self):
        return self.name[0]

    @property
    def vector(self) -> tuple[int, int]:
        mapping = {
            Direction.NORTH: (0, -1),
            Direction.SOUTH: (0, 1),
            Direction.EAST:  (1, 0),
            Direction.WEST:  (-1, 0),
        }
        return mapping[self]

    @property
    def opposite(self) -> "Direction":
        mapping = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST:  Direction.WEST,
            Direction.WEST:  Direction.EAST,
        }
        return mapping[self]


class Cell:
    def __init__(self, wall_graphics: WallGraphics, walls: int = 0xF,
                 invicible_walls: int = 0x0) -> None:
        self.invincible_walls: int = invicible_walls
        self.walls: int = walls
        self.wall_graphics = wall_graphics

    def HasWall(self, dir: Direction) -> bool:
        return ((self.walls | self.invincible_walls) & dir) != 0

    def __setitem__(self, d: Direction, value: bool):
        if not value and self.invincible_walls & d != 0:
            raise InvalidCellOperation("Tried deleting and invincible wall")
        self.walls = (self.walls | d) if value else (self.walls & ~d)

    def Serialize(self) -> str:
        return str(hex(self.walls | self.invincible_walls))

    def __iadd__(self, dir: Direction) -> "Cell":
        self.walls |= dir
        return self

    @staticmethod
    def AddWall(walls: int, dir: Direction) -> int:
        return walls | dir


# Directly modifying a cell is dangerous cause the maze could become incoherent
class ReadonlyCell:
    def __init__(self, cell: Cell) -> None:
        self.cell = cell

    @property
    def walls(self):
        return self.cell.walls

    @property
    def invincible_walls(self):
        return self.cell.invincible_walls
