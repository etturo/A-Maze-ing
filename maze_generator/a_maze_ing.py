#!/usr/bin/env python3
from maze_generator import SettingsReader, MazeSettings, Maze


def a_maze_ing():
    settings: MazeSettings = SettingsReader().Read()
    print(settings.settings)
    maze = Maze(settings)
    print(maze.serialize())


if __name__ == "__main__":
    a_maze_ing()
