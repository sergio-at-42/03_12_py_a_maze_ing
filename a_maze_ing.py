#!/usr/bin/env python3

import sys
from typing import Any, Self

from Maze import Maze


def main() -> None:
    my_maze: Maze = Maze(sys.argv)

if __name__ == "__main__":
    main()
