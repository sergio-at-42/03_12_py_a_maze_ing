from typing import Any, Self
from pydantic import BaseModel, Field, ValidationError, model_validator

from .coord import Coord


class MazeConfig(BaseModel):

    config_file_name: str = Field(default="config.txt")
    width: int = Field(default=16)
    height: int = Field(default=16)
    entry: Coord = Coord(x=0, y=0)
    exit:  Coord = Coord(x=15, y=15)
    output_file: str = Field(default="maze.txt")
    perfect: bool = Field(default=True)
    attr: dict[str, Any] = {}

    @model_validator(mode='after')
    def config_read_file(self) -> "MazeConfig":
        config_line: str = ""
        try:
            with open(self.config_file_name, "r") as config_file:
                self.attr["CONFIGURATION_FILE_NAME"] = (self.config_file_name)
                config_line = config_file.readline()
                while config_line:
                    key = config_line.partition("=")[0]
                    value = config_line.partition("=")[2]
                    self.set_value_to_attr(key, value)
                    config_line = config_file.readline()
        except FileNotFoundError:
            print(f"<{self.config_file_name}> is not a configuration file.")
        return (self)

    def set_value_to_attr(self, key: str, value: Any) -> bool:
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

    def config_display(self) -> None:
        print("Configuration attributes :")
        print(f"CONFIGURATION_FILE_NAME = {self.config_file_name}")
        print(f"WIDTH = {self.width}")
        print(f"HEIGHT = {self.height}")
        print(f"ENTRY = {(self.entry.x, self.entry.y)}")
        print(f"EXIT = {(self.exit.x, self.exit.y)}")
        print(f"OUTPUT_FILE = {self.output_file}")
        print(f"PERFECT = {self.perfect}")
        print("Configuration attributes dictionary :")
        print(f"obj.config.attr = {self.attr}")



# Brouillon ;-)


        # # attributs de configurations
        # self.width: int = 16
        # self.height: int = 16
        # self.entry: Coord = Coord(x=0, y=0)
        # self.exit:  Coord = Coord(x=15, y=15)
        # self.output_file: str = "maze.txt"
        # self.perfect: bool = True

        # Dictionnaire de l'ensemble des attributs de configuration
        # self.attr: dict[str, Any] = {}


    # def config_attr_to_dict(self) -> None:
    #     self.attr["WIDTH"] = self.width
    #     self.attr["HEIGHT"] = self.height
    #     self.attr["ENTRY"] = (self.entry.x, self.entry.y)
    #     self.attr["EXIT"] = (self.exit.x, self.exit.y)
    #     self.attr["OUTPUT_FILE"] = self.output_file
    #     self.attr["PERFECT"] = self.perfect


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


# from enum import Enum

# class ConfigAttr(Enum):

#     WIDTH = "width"
#     HEIGHT = "height"
#     ENTRY = "entry"
#     EXIT = "exit"
#     OUTPUT_FILE = "output_file"
#     PERFECT = "perfect"


