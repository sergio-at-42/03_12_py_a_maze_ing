#!/usr/bin/env python3

import sys
from typing import TextIO


def read_config(argv: list[str]) -> bool:
    error = False
    file_name: str = ""
    config_line: str = ""
    try:
        file_name = argv[1]
        config_file: TextIO = open(file_name)
        config_line = config_file.readline()
        while config_line:
            print(config_line, end="")
            config_line = config_file.readline()
        config_file.close()
    except IndexError:
        print("No configuration file provide.")
        print(f"Usage: {argv[0].rpartition("/")[2]} <configuration_file>")
        error = True
    except FileNotFoundError:
        print(f"<{file_name}> is not a configuration file.")
        print(f"Usage: {argv[0].rpartition("/")[2]} <configuration_file>")
        error = True
    return error

def main() -> None:
    read_config(sys.argv)

if __name__ == "__main__":
    main()
