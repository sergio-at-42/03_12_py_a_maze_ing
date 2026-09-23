from time import sleep

from .maze_config import MazeConfig
from .wall import Wall
from .coord import Coord
from .color import Color
from .wall_type import WallType


class MazePath():

    def __init__(self, maze_config: MazeConfig) -> None:
        self.maze_config: MazeConfig = maze_config
        self.pos: Coord = Coord(x=self.maze_config.entry.x,
                                y=self.maze_config.entry.y)
        self.old_p: Coord = Coord(x=self.pos.x, y=self.pos.y)
        self.wall: Wall = Wall(WallType.SIMPLE, Color.CYAN, Color.BG_BLACK)
        self.visible: bool = False
        self.speed: int = 0
        self.direction: list[str] = []

    def display(self) -> None:
        self.display_entry()
        self.display_exit()
        self.pos.x = self.maze_config.entry.x + 1
        self.pos.y = self.maze_config.entry.y + 1
        for d in self.direction:
            self.old_p.x = self.pos.x
            self.old_p.y = self.pos.y
            sleep(self.speed / 100)
            match d:
                case "N":
                    if self.pos.y > 1:
                        self.pos.y -= 1
                        self.display_north()
                case "S":
                    if self.pos.y < self.maze_config.height:
                        self.pos.y += 1
                        self.display_south()
                case "E":
                    if self.pos.x < self.maze_config.width:
                        self.pos.x += 1
                        self.display_east()
                case "W":
                    if self.pos.x > 1:
                        self.pos.x -= 1
                        self.display_west()
        self.speed = 0

    def display_east(self) -> None:
        print(f"\033[{self.pos.y * 2};{self.pos.x * 3 - 1}H", end="")
        print(f"{self.maze_config.toto_icon}", end="")
        print(f"\033[{self.old_p.y * 2};{self.old_p.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_west(self) -> None:
        print(f"\033[{self.pos.y * 2};{self.pos.x * 3 - 1}H", end="")
        print(f"{self.maze_config.toto_icon}", end="")
        print(f"\033[{self.old_p.y * 2};{self.old_p.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_north(self) -> None:
        print(f"\033[{self.pos.y * 2};{self.pos.x * 3 - 1}H", end="")
        print(f"{self.maze_config.toto_icon}", end="")
        print(f"\033[{self.old_p.y * 2};{self.old_p.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"\033[{self.old_p.y * 2 - 1};{self.old_p.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_south(self) -> None:
        print(f"\033[{self.pos.y * 2};{self.pos.x * 3 - 1}H", end="")
        print(f"{self.maze_config.toto_icon}", end="")
        print(f"\033[{self.old_p.y * 2};{self.old_p.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"\033[{self.old_p.y * 2 + 1};{self.old_p.x * 3 - 1}H", end="")
        print(f"{self.maze_config.path_icon}")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_entry(self) -> None:
        print(f"\033[{(self.maze_config.entry.y + 1) * 2};{(
            self.maze_config.entry.x + 1) * 3 - 1}H", end="")
        print(f"{Color.RED.value}{Color.BOLD.value}", end="")
        print(f"{self.maze_config.entry_icon}", end="")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

    def display_exit(self) -> None:
        print(f"\033[{(self.maze_config.exit.y + 1) * 2};{(
            self.maze_config.exit.x + 1) * 3 - 1}H", end="")
        print(f"{Color.MAGENTA.value}{Color.BOLD.value}", end="")
        print(f"{self.maze_config.exit_icon}", end="")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")
