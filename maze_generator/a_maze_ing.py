#!/usr/bin/env python3
from maze_generator import SettingsReader, MazeSettings, Maze
import sys


def a_maze_ing() -> None:
    settings: MazeSettings = SettingsReader().Read(
        sys.argv[1] if len(sys.argv) > 1 else None)
    maze = Maze(settings)
    maze.serialize()


if __name__ == "__main__":
    a_maze_ing()
