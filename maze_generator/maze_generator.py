from abc import ABC, abstractmethod
from typing import Callable
from maze_generator.maze import Maze


class MazeGenerator(ABC):
    def __init__(self, settings: dict[str, str]):
        self._settings: dict[str, str] = settings
        self.OnSnapshot: Callable
        self.OnStart: Callable
        return

    @abstractmethod
    def Generate(self) -> Maze:
        pass
