#!/usr/bin/env python3

import sys
from typing import Any, TextIO


class MazeConfig:

    def __init__(self, argv: list[str]) -> None:
            self.key: dict[str, Any] = {
                    "WIDTH": 16,
                    "HEIGHT": 16,
                    "ENTRY": list([0, 0]),
                    "EXIT": list([15, 15]),
                    "OUTPUT_FILE": "maze.txt",
                    "PERFECT": True
                }
            self.read_config(argv)
    
    def read_config(self, argv: list[str]) -> bool:
        error = False
        file_name: str = ""
        config_line: str = ""
        try:
            file_name = argv[1]
            config_file: TextIO = open(file_name)
            config_line = config_file.readline()
            while config_line:
                if config_line[0] != "#":
                    key = config_line.partition("=")[0]
                    match key:
                        case "WIDTH":
                            self.key[key] = config_line.partition("=")[2]

                                case _:

                                
                    self.key[k] = config_line.partition("=")[2]
                    print(config_line, end="")
                    print(self.key[key])
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
    cfg: MazeConfig = MazeConfig(sys.argv)

if __name__ == "__main__":
    main()
