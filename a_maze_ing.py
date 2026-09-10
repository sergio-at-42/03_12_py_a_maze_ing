#!/usr/bin/env python3

import sys
from typing import Any, Self

from libmaze import Maze


def main() -> None:

    my_maze: Maze = Maze()

    my_maze.config.config_display()

if __name__ == "__main__":
    main()
