from typing import Any
import sys
from pydantic import BaseModel, Field, model_validator

from .color import Color
from .wall_type import WallType
from .coord import Coord
from mazegen import PATTERN_H, PATTERN_W
from .maze_error import EntryIn42Error, EntryNotInMaze, ExitegalEntry, \
    ExitIn42Error, ExitNotInMaze, WidthLessThan0Error, \
    HeightLessThan0Error, MazeError, WidthSmallFor42Error, \
    HeightToSmallFor42Error


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
    msg_error: str = ""
    msg_error_generator: str = ""
    pattern42: set[tuple[int, int]] = set()
    attr: dict[str, Any] = {}

    @model_validator(mode='after')
    def config_read_file(self) -> "MazeConfig":
        self.file_from_argv()
        config_line: str = ""
        try:
            with open(self.config_file_name, "r") as config_file:
                config_line = config_file.readline()
                while config_line:
                    key = config_line.partition("=")[0].strip()
                    value = config_line.partition("=")[2].strip()
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

    def set_value_to_attr(self, key: str, value: str) -> bool:
        coord: list[str] = []
        value_ok = True
        key = key.upper()
        try:
            match key:
                case "WIDTH":
                    self.width = int(value)
                    if self.width < 0:
                        raise WidthLessThan0Error
                    if self.width < PATTERN_W + 2:
                        raise WidthSmallFor42Error
                case "HEIGHT":
                    self.height = int(value)
                    if self.height < 0:
                        raise HeightLessThan0Error
                    if self.height < PATTERN_H + 2:
                        raise HeightToSmallFor42Error
                case "ENTRY":
                    coord = list(value.partition(","))
                    self.entry.x = int(coord[0])
                    self.entry.y = int(coord[2])
                    if not (0 <= self.entry.x < self.width
                            and 0 <= self.entry.y < self.height):
                        raise EntryNotInMaze
                    if (self.entry.x, self.entry.y) in self.pattern42:
                        raise EntryIn42Error
                    if (self.entry.x, self.entry.y) == \
                            (self.exit.x, self.exit.y):
                        raise ExitegalEntry
                case "EXIT":
                    coord = list(value.partition(","))
                    self.exit.x = int(coord[0])
                    self.exit.y = int(coord[2])
                    if not (0 <= self.exit.x < self.width
                            and 0 <= self.exit.y < self.height):
                        raise ExitNotInMaze
                    if (self.exit.x, self.exit.y) in self.pattern42:
                        raise ExitIn42Error
                    if (self.entry.x, self.entry.y) == \
                            (self.exit.x, self.exit.y):
                        raise ExitegalEntry
                case "OUTPUT_FILE":
                    self.output_file = value.strip()
                case "PERFECT":
                    self.perfect = False if value.strip().upper() == "FALSE"\
                        else True
                case "SEED":
                    self.seed = int(value)
                case _:
                    value_ok = False
        except ValueError:
            self.msg_error += "Value error in your configuration file, stupid user.\n"
        except MazeError as e:
            self.msg_error += f"{e}\n"
            try:
                raise e
            except WidthLessThan0Error:
                self.width = 16
            except HeightLessThan0Error:
                self.height = 16
            except EntryNotInMaze:
                self.entry.x = 0
                self.entry.y = 0
            except ExitNotInMaze:
                self.exit.x = self.width - 1
                self.exit.y = self.height - 1
            except ExitegalEntry:
                self.entry.x = 0
                self.entry.y = 0
                self.exit.x = self.width - 1
                self.exit.y = self.height - 1
            except EntryIn42Error:
                self.entry.x = 0
                self.entry.y = 0
            except ExitIn42Error:
                self.exit.x = self.width - 1
                self.exit.y = self.height - 1
            except WidthSmallFor42Error, HeightToSmallFor42Error:
                pass
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
