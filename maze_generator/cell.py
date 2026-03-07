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

    # Pretty sure this could be written better, logic is ok though
    def GetGraphics(self, dir: Direction) -> str:
        match (dir):
            case Direction.NORTH:
                return (self.wall_graphics.top
                        if self.HasWall(Direction.NORTH) else " ")
            case Direction.EAST:
                return (self.wall_graphics.left
                        if self.HasWall(Direction.EAST) else " ")
            case Direction.SOUTH:
                return (self.wall_graphics.top
                        if self.HasWall(Direction.SOUTH) else " ")
            case Direction.WEST:
                return (self.wall_graphics.left
                        if self.HasWall(Direction.WEST) else " ")

    def Serialize(self) -> str:
        return str(hex(self.walls | self.invincible_walls))

    @staticmethod
    def AddWall(walls: int, dir: Direction) -> int:
        return walls | dir
