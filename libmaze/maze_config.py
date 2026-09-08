from email.policy import default
from typing import Any, Self
from pydantic import BaseModel, Field, ValidationError, model_validator
from .coord import Coord


class MazeConfig(BaseModel):

    def __init__(self, config_file_name: str) -> None:
        # attributs de configurations
        self.width: int = Field(..., ge=0, default=16)
        self.height: int = Field(..., ge=0, default=16)
        self.entry: Coord = Coord(0, 0)
        self.exit:  Coord = Coord(15, 15)
        self.output_file: str = Field(..., default="maze.txt")
        self.perfect: bool = Field(default=True)

        # Dictionnaire de l'ensemble des attributs de configuration
        self.attr: dict[str, Any] = {}

        # Initialisation des attributs de configuration depuis un fichier de configuration
        self.config_read_file(config_file_name)

    def config_read_file(self, config_file_name: str) -> bool:
        error = False
        config_line: str = ""
        try:
            with open(config_file_name, "r") as config_file:
                config_line = config_file.readline()
                while config_line:
                    key = config_line.partition("=")[0]
                    value = config_line.partition("=")[2]
                    if self.config_value_to_attr(key, value):
                        print(key, self.attr[key])
                    config_line = config_file.readline()
        except FileNotFoundError:
            print(f"<{config_file_name}> is not a configuration file.")
            error = True
        return error

    def config_value_to_attr(self, key: str, value: Any) -> bool:
        value_ok = True
        key = key.upper()
        match key:
            case "WIDTH":
                self.width = int(value)
                self.attr["WIDTH"] = self.width
            case "HEIGHT":
                self.height = int(value)
                self.attr["HEIGHT"] = self.height
            case "ENTRY":
                coord: list[str] = value.partition(",")
                self.entry.x = int(coord[0])
                self.entry.y = int(coord[2])
                self.attr["ENTRY"] = (self.entry.x, self.entry.y)
            case "EXIT":
                coord: list[str] = value.partition(",")
                self.exit.x = int(coord[0])
                self.exit.y = int(coord[2])
                self.attr["EXIT"] = (self.exit.x, self.exit.y)
            case "OUTPUT_FILE":
                self.output_file = value.strip()
                self.attr["OUTPUT_FILE"] = self.output_file
            case "PERFECT":
                self.perfect = bool(value)
                self.attr["PERFECT"] = self.perfect
            case _:
                value_ok = False
        return (value_ok)






    # def config_attr_to_dict(self) -> None:
    #     self.attr["WIDTH"] = self.width
    #     self.attr["HEIGHT"] = self.height
    #     self.attr["ENTRY"] = (self.entry.x, self.entry.y)
    #     self.attr["EXIT"] = (self.exit.x, self.exit.y)
    #     self.attr["OUTPUT_FILE"] = self.output_file
    #     self.attr["PERFECT"] = self.perfect



# Brouillon ;-)

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
