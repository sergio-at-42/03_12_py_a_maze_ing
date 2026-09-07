from typing import Any, Self


class Maze:

    def __init__(self, argv: list[str]) -> None:
        self.config: dict[str, Any] = {
            "WIDTH": 16,
            "HEIGHT": 16,
            "ENTRY": [0, 0],
            "EXIT": [15, 15],
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": True
        }
        self.config_read_file(argv)

    def config_value_to_dict(self, key: str, value: Any) -> bool:
        error = False
        key = key.upper()
        if key not in self.config:
            return (error)
        error = True
        match key:
            case "WIDTH":
                self.config[key] = int(value)
            case "HEIGHT":
                self.config[key] = int(value)
            case "ENTRY":
                coord: list[str] = value.partition(",")
                self.config[key] = [int(coord[0]), int(coord[2])]
            case "EXIT":
                coord: list[str] = value.partition(",")
                self.config[key] = [int(coord[0]), int(coord[2])]
            case "OUTPUT_FILE":
                self.config[key] = value.strip()
            case "PERFECT":
                self.config[key] = bool(value)
        return (error)

    def config_read_file(self, argv: list[str]) -> bool:
        error = False
        file_name: str = ""
        config_line: str = ""
        try:
            with open(argv[1], "r") as config_file:
                config_line = config_file.readline()
                while config_line:
                    # if config_line[0] != "#":
                    key = config_line.partition("=")[0]
                    value = config_line.partition("=")[2]
                    if self.config_value_to_dict(key, value):
                        print(key, self.config[key])
                    config_line = config_file.readline()
        except IndexError:
            print("No configuration file provide.")
            print(f"Usage: {argv[0].rpartition("/")[2]} <configuration_file>")
            error = True
        except FileNotFoundError:
            print(f"<{argv[1]}> is not a configuration file.")
            print(f"Usage: {argv[0].rpartition("/")[2]} <configuration_file>")
            error = True
        return error




# Brouillon ;-)

        # self.width: int = 16
        # self.height: int = 16
        # self.entry: list[int] = [0, 0]
        # self.exit: list[int] = [15, 15]
        # self.output_file: str = "maze.txt"
        # self.perfect: bool = True
        # self.key: dict[str, Any] = {}

    # def set_width(self, width: int) -> Self:
        # self.width = width
        # return (self)
# 
    # def set_height(self, height: int) -> Self:
        # self.height = height
        # return (self)
# 
    # def set_entry(self, entry: list[int]) -> Self:
        # self.entry = entry
        # return (self)
# 
    # def set_exit(self, exit: list[int]) -> Self:
        # self.exit = exit
        # return (self)
# 
    # def set_output_file(self, output_file: str) -> Self:
        # self.output_file = output_file
        # return (self)
# 
    # def set_perfect(self, perfect: bool) -> Self:
        # self.perfect = perfect
        # return (self)
