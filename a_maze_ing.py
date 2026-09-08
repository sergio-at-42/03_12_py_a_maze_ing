#!/usr/bin/env python3

import sys
from typing import Any, Self

from libmaze import Maze


def config_file_exist(argv: list[str]) -> str:
    file_name: str = ""
    try:
        with open(argv[1], "r") as config_file:
            file_name = argv[1]
    except IndexError:
        print("No configuration file provide.")
        print(f"Usage: {argv[0].rpartition("/")[2]} <configuration_file>")
    except FileNotFoundError:
        print(f"<{argv[1]}> is not a configuration file.")
        print(f"Usage: {argv[0].rpartition("/")[2]} <configuration_file>")
    return (file_name)

def main() -> None:
    config_file_name: str = config_file_exist(sys.argv)
    if config_file_name:
        my_maze: Maze = Maze(config_file_name)

if __name__ == "__main__":
    main()
