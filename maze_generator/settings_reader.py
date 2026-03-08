from enum import IntEnum


class InvalidFormat(Exception):
    pass


class WallType(IntEnum):
    TOP_LEFT = 0
    TOP_CROSS = 1
    TOP = 2
    TOP_RIGHT = 3
    RIGHT = 4
    LEFT = RIGHT
    BOT = TOP
    LEFT_CROSS = 5
    CROSS = 6
    RIGHT_CROSS = 7
    BOT_LEFT = 8
    BOT_CROSS = 9
    BOT_RIGHT = 10


class WallGraphics():
    def __init__(self, wall_str: str) -> None:
        self.__graphics: dict[WallType, str] = dict()
        for key in WallType:
            self.__graphics[key] = wall_str[key]

    def __getitem__(self, key: WallType):
        return self.__graphics[key]


class MazeSettings:
    def __check_validity(self, mandatory: list[str]) -> None:
        for element in mandatory:
            if (self.settings.get(element) is None):
                raise InvalidFormat(f"Missing {element} field")

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


defaultSettings: MazeSettings = MazeSettings({'WIDTH': '20',
                                              'HEIGHT': '15',
                                              'ENTRY': '0,0',
                                              'EXIT': '20,15',
                                              'OUTPUT_FILE': 'output_maze.txt',
                                              'PERFECT': 'FALSE',
                                              'WALL_CHARACTERS':
                                              '╔╦═╗║╠═╬╣╚╩═╝'})
