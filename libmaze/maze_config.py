from typing import Any
import sys
from pydantic import BaseModel, Field, model_validator

from .color import Color
from .wall_type import WallType
from .coord import Coord


class MazeConfig(BaseModel):

    width: int = Field(ge=0, default=16)
    height: int = Field(ge=0, default=16)
    entry: Coord = Coord(x=2, y=2)
    exit:  Coord = Coord(x=15, y=15)
    output_file: str = Field(default="maze.txt")
    perfect: bool = Field(default=False)
    argv: list[str] = []
    config_file_name: str = Field(default="")
    seed: int = Field(ge=0, default=16)
    entry_icon: str = "🏁"                  # U\0001F3C1
    exit_icon: str = "🍾"                   # U\0001F37E
    toto_icon: str = "\U0001F6BD"           # "\U0001F6BD" "\U0001F47E"
    path_icon: str = "\U0001F4A9"           # "\U0001F4A9"
    wall_type: WallType = WallType.SIMPLE
    wall_color: Color = Color.YELLOW
    wall_bkcolor: Color = Color.BG_BLUE
    attr: dict[str, Any] = {}

    @model_validator(mode='after')
    def config_read_file(self) -> "MazeConfig":
        self.file_from_argv()
        config_line: str = ""
        try:
            with open(self.config_file_name, "r") as config_file:
                config_line = config_file.readline()
                while config_line:
                    key = config_line.partition("=")[0]
                    value = config_line.partition("=")[2]
                    self.set_value_to_attr(key, value)
                    config_line = config_file.readline()
        except FileNotFoundError:
            print("No configuration file found.")
        self.set_attr_to_dict()
        return (self)

    def file_from_argv(self) -> None:
        try:
            self.argv = sys.argv
            with open(self.argv[1], "r"):
                self.config_file_name = self.argv[1]
        except IndexError:
            print("No configuration file provide.")
            print(f"Usage: {self.argv[0].rpartition("/")[2]} <conf_file>")
            print("Default values used to create the maze.")
        except FileNotFoundError:
            print(f"<{self.argv[1]}> is not a configuration file.")
            print(f"Usage: {self.argv[0].rpartition("/")[2]} <conf_file>")
            print("Default values used to create the maze.")

    def set_value_to_attr(self, key: str, value: Any) -> bool:
        coord: list[str] = []
        value_ok = True
        key = key.upper()
        match key:
            case "WIDTH":
                self.width = int(value)
            case "HEIGHT":
                self.height = int(value)
            case "ENTRY":
                coord = value.partition(",")
                self.entry.x = int(coord[0])
                self.entry.y = int(coord[2])
            case "EXIT":
                coord = value.partition(",")
                self.exit.x = int(coord[0])
                self.exit.y = int(coord[2])
            case "OUTPUT_FILE":
                self.output_file = value.strip()
            case "PERFECT":
                self.perfect = False if value.strip().upper() == "FALSE"\
                    else True
            case "SEED":
                self.seed = int(value)
            case _:
                value_ok = False
        return (value_ok)

    def set_attr_to_dict(self) -> None:
        self.attr["WIDTH"] = self.width
        self.attr["HEIGHT"] = self.height
        self.attr["ENTRY"] = (self.entry.x, self.entry.y)
        self.attr["EXIT"] = (self.exit.x, self.exit.y)
        self.attr["OUTPUT_FILE"] = self.output_file
        self.attr["PERFECT"] = self.perfect
        self.attr["ARGV"] = (self.argv)
        self.attr["CONFIGURATION_FILE_NAME"] = (self.config_file_name)
        self.attr["SEED"] = self.seed

    def config_display(self) -> None:
        print("Configuration attributes :")
        print(f"ARGV = {self.argv}")
        print(f"CONFIGURATION_FILE_NAME = {self.config_file_name}")
        print(f"WIDTH = {self.width}")
        print(f"HEIGHT = {self.height}")
        print(f"ENTRY = {(self.entry.x, self.entry.y)}")
        print(f"EXIT = {(self.exit.x, self.exit.y)}")
        print(f"OUTPUT_FILE = {self.output_file}")
        print(f"PERFECT = {self.perfect}")
        print(f"SEED = {self.seed}")
        print("Configuration attributes dictionary :")
        print(f"obj.config.attr = {self.attr}")
