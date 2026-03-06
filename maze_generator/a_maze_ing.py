#!/usr/bin/env python3
from maze_generator import SettingsReader, MazeSettings, Maze


def a_maze_ing() -> None:
    settings: MazeSettings = SettingsReader().Read("tests/test_configs.txt")
    maze = Maze(settings)
    maze.serialize()


if __name__ == "__main__":
    a_maze_ing()
