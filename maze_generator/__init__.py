__name__ = "A-Maze-ing"
__version__ = "1.0.0"
__authors__ = ("lavverat", "eturini")

__all__ = ['Cell',
           'Direction',
           'MazeGenerator',
           'Maze',
           'MazeSettings',
           'SettingsReader',
           'InvalidFormat']


from maze_generator.cell import (Cell,
                                 Direction)
# from maze_generator.a_maze_ing import
from maze_generator.maze_generator import MazeGenerator
from maze_generator.maze import Maze
from maze_generator.settings_reader import (MazeSettings,
                                            SettingsReader,
                                            InvalidFormat)

# TODO: Setup package names and other stuff as subjects wants
