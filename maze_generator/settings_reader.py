

class InvalidFormat(Exception):
    pass


class MazeSettings:
    def __check_validity(self, mandatory: list[str]) -> None:
        for element in mandatory:
            if (self.settings.get(element) is None):
                raise InvalidFormat(f"Missing {element} field")

    def __init__(self, settings: dict[str, str]) -> None:
        self.settings = settings
        self.__check_validity(["WIDTH", "HEIGHT", "ENTRY",
                               "EXIT", "OUTPUT_FILE", "PERFECT"])

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
        try:
            if path is None:
                return defaultSettings
            with open(path, "r") as file:
                settings: dict[str, str] = dict[str, str]()
                for line in file:
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
                                              'PERFECT': 'FALSE'})
