from enum import IntEnum
from maze_generator.settings_reader import WallGraphics, WallType


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

    @staticmethod
    def DirectionToWall(dir: Direction) -> WallType:
        match(dir):
            case Direction.NORTH: return WallType.TOP
            case Direction.WEST: return WallType.LEFT
            case Direction.EAST: return WallType.RIGHT
            case Direction.SOUTH: return WallType.BOT

    def HasWall(self, dir: Direction) -> bool:
        return ((self.walls | self.invincible_walls) & dir) != 0

    def __setitem__(self, d: Direction, value: bool):
        if not value and self.invincible_walls & d != 0:
            raise InvalidCellOperation("Tried deleting and invincible wall")
        self.walls = (self.walls | d) if value else (self.walls & ~d)

    def Serialize(self) -> str:
        return str(hex(self.walls | self.invincible_walls))

    def GetWallSprite(self, dir: Direction) -> str:
        return self.wall_graphics[self.DirectionToWall(dir)] if self.HasWall(dir) else " "

    @staticmethod
    def AddWall(walls: int, dir: Direction) -> int:
        return walls | dir
