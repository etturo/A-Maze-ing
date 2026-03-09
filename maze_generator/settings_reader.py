from enum import IntEnum


class InvalidFormat(Exception):
    pass


class WallType(IntEnum):
    EMPTY = 0
    # Straight/Ends
    NORTH_ONLY = 1
    EAST_ONLY = 2
    SOUTH_ONLY = 4
    WEST_ONLY = 8
    # Corners
    BOT_RIGHT = 9   # North(1) + East(2)
    TOP_RIGHT = 12   # East(2) + South(4)
    TOP_LEFT = 6  # South(4) + West(8)
    BOT_LEFT = 3   # West(8) + North(1)
    # Straights
    VERTICAL = 5   # North(1) + South(4)
    HORIZONTAL = 10  # East(2) + West(8)
    # T-Crosses
    T_DOWN = 14  # E(2)+S(4)+W(8)
    T_UP = 11  # W(8)+N(1)+E(2)
    T_LEFT = 13  # N(1)+S(4)+W(8)
    T_RIGHT = 7   # N(1)+E(2)+S(4)
    # Full Cross
    CROSS = 15  # N+E+S+W


class WallGraphics():
    def __init__(self, wall_str: str) -> None:
        self.__graphics: dict[WallType, str] = dict()
        for key in WallType:
            self.__graphics[key] = wall_str[key]

    def __getitem__(self, key: WallType):
        return self.__graphics[key]


class MazeSettings:
    def __inside(self, t: tuple[int, int]) -> bool:
        return (t[0] > int(self.settings["WIDTH"]) or
                t[0] < 0 or
                t[1] > int(self.settings["HEIGHT"]) or
                t[1] < 0)

    def __check_validity(self, mandatory: list[str]) -> None:
        for element in mandatory:
            if (self.settings.get(element) is None):
                raise InvalidFormat(f"Missing {element} field")
        if self.__inside(SettingsReader.CommaToTuple(self.settings["ENTRY"])):
            raise InvalidFormat(f"Invalid 'ENTRY': {element}")
        if self.__inside(SettingsReader.CommaToTuple(self.settings["EXIT"])):
            raise InvalidFormat(f"Invalid 'EXIT': {element}")

    def __init__(self, settings: dict[str, str]) -> None:
        self.settings = settings
        self.__check_validity(["WIDTH", "HEIGHT", "ENTRY",
                               "EXIT", "OUTPUT_FILE", "PERFECT"])
        self.wall_graphics: WallGraphics = \
            WallGraphics(settings["WALL_CHARACTERS"])

    def __getitem__(self, key: str) -> str:
        return self.settings[key]


class SettingsReader:
    @staticmethod
    def __split_line(line: str) -> tuple[str, str]:
        try:
            key, value = line.strip().split('=')
            return key, value
        except ValueError as e:
            raise InvalidFormat(f"Invalid format in line: '{line}'") from e

    @staticmethod
    def Read(path: str | None) -> MazeSettings:
        if path is None:
            return defaultSettings
        try:
            with open(path, "r") as file:
                settings: dict[str, str] = dict[str, str]()
                for line in file:
                    if (line.isspace() or line.strip().startswith("#")):
                        continue
                    try:
                        key, value = SettingsReader.__split_line(line)
                        settings[key] = value
                    except InvalidFormat as e:
                        print(e)
            return MazeSettings(settings)
        except (FileNotFoundError, FileExistsError, PermissionError):
            print(f"Couldn't open {path}")
            return defaultSettings

    @staticmethod
    def CommaToTuple(comma: str) -> tuple[int, int]:
        return tuple(map(int, comma.split(',')))


defaultSettings: MazeSettings = MazeSettings({'WIDTH': '20',
                                              'HEIGHT': '15',
                                              'ENTRY': '0,0',
                                              'EXIT': '20,15',
                                              'OUTPUT_FILE': 'output_maze.txt',
                                              'PERFECT': 'FALSE',
                                              'WALL_CHARACTERS':
                                              ' ╨╞╚╥║╔╠╡╝═╩╗╣╦╬'})
