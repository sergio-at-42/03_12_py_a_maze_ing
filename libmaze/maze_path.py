from time import sleep
from typing import Any, Self

from .maze_config import MazeConfig
from .wall import Wall
from .coord import Coord
from .color import Color
from .wall_type import WallType


class MazePath():

    def __init__(self, maze_config: MazeConfig) -> None:
        self.maze_config: MazeConfig = maze_config
        # self.entry: Coord = maze_config.entry
        # self.exit:  Coord = maze_config.exit
        self.position: Coord = Coord(x = self.maze_config.entry.x, y = self.maze_config.entry.y)
        self.old_position: Coord = Coord(x = self.position.x, y = self.position.y)
        self.wall: Wall = Wall(WallType.SIMPLE, Color.CYAN, Color.BG_BLACK)
        self.wall_path: str = ""
        self.visible:bool = False
        self.speed: int = 0
        # self.entry_icon: str = "🏁" # U+1F3C1
        # self.exit_icon: str = "🍾" # U+1F37E
        self.direction: str = "EEEEESSSSSSEEEEEEEEEEEEEEESSSSSSSSSSSWWWNNNNWWWWWWWWWWSSSSSSSSSEEESWWWEENNNNNNNWSSWWWWWWWWWSSSSEEEEEEEEEEEEEEEEEEEEEEEES"

    def display(self) -> None:
        self.display_entry()
        self.display_exit()
        self.position.x = self.maze_config.entry.x
        self.position.y = self.maze_config.entry.y
        for d in self.direction:
            self.old_position.x = self.position.x
            self.old_position.y = self.position.y
            sleep(self.speed / 100)
            match d:
                case "N":
                    if self.position.y > 1:
                        self.position.y -= 1
                        self.display_north()
                        # self.wall_path = self.wall.construct(1)
                case "S":
                    if self.position.y < self.maze_config.height:
                        self.position.y += 1
                        self.display_south()
                        # self.wall_path = self.wall.construct(1)
                case "E":
                    if self.position.x < self.maze_config.width:
                        self.position.x += 1
                        self.display_east()
                        # self.wall_path = f"{self.wall.construct(2) * 3}"
                case "W":
                    if self.position.x > 1:
                        self.position.x -= 1
                        self.display_west()
                        # self.wall_path = f"{self.wall.construct(2) * 3}"
            # self.display_position()
        self.speed = 0

    def display_east(self) -> None:
        print(f"\033[{self.position.y * 2};{self.position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.toto_icon}", end="")
        print(f"\033[{self.old_position.y * 2};{self.old_position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_west(self) -> None:
        print(f"\033[{self.position.y * 2};{self.position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.toto_icon}", end="")
        print(f"\033[{self.old_position.y * 2};{self.old_position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_north(self) -> None:
        print(f"\033[{self.position.y * 2};{self.position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.toto_icon}", end="")
        print(f"\033[{self.old_position.y * 2};{self.old_position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"\033[{self.old_position.y * 2 - 1};{self.old_position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_south(self) -> None:
        print(f"\033[{self.position.y * 2};{self.position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.toto_icon}", end="")
        print(f"\033[{self.old_position.y * 2};{self.old_position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"\033[{self.old_position.y * 2 + 1};{self.old_position.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_entry(self) -> None:
        print(f"\033[{self.maze_config.entry.y * 2};{self.maze_config.entry.x * 3 - 1}H", end="")
        print(f"{Color.RED.value}{Color.BOLD.value}{self.maze_config.entry_icon}{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_exit(self) -> None:
        print(f"\033[{self.maze_config.exit.y * 2};{self.maze_config.exit.x * 3 - 1}H", end="")
        print(f"{Color.MAGENTA.value}{Color.BOLD.value}{self.maze_config.exit_icon}{Color.RESET.value}{Color.CURSOR_OFF.value}")


    # def display_position(self) -> None:
    #     print(f"\033[{self.position.y * 2};{self.position.x * 3 - 1}H", end="")
    #     print(f"{self.maze_config.toto_icon}", end="")
    #     print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")
    #     self.display_old_position()

    # def display_old_position(self) -> None:
    #     print(f"\033[{self.old_position.y * 2};{self.old_position.x * 3 - 1}H", end="")
    #     print(f"{Color.RED.value}{self.maze_config.path_icon}{Color.RESET.value}{Color.CURSOR_OFF.value}")
