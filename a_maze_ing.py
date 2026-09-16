#!/usr/bin/env python3

import sys
from typing import Any, Self

from libmaze import Maze


def main() -> None:

    my_maze: Maze = Maze()

    # my_maze.config.config_display()
    my_maze.display()

    my_maze.write_output_file()

    print(f"\033[{my_maze.config.height*2+7};1H", end="")

if __name__ == "__main__":
    main()
