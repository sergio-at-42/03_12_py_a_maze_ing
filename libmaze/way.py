from typing import Any, Self

from .wall import Wall
from .coord import Coord
from .color import Color


class Way():

    def __init__(self, entry: Coord = Coord(x=2, y=2), exit: Coord = Coord(x=15, y=15)) -> None:
        self.entry: Coord = entry
        self.exit:  Coord = exit
        self.entry_icon: str = "🏁" # U+1F3C1
        self.exit_icon: str = "🍾" # U+1F37E
        self.direction: str = "NNWWWSSSSSSWWWNNNNWSSSSSSSSSEEESWWWWWWNWSS"

    def display(self) -> None:
        self.display_entry()
        self.display_exit()


    def display_entry(self) -> None:
        print(f"\033[{self.entry.y * 2};{self.entry.x * 3 - 1}H", end="")
        print(f"{Color.RED.value}{Color.BOLD.value}{self.entry_icon}{Color.RESET.value}", end="")

    def display_exit(self) -> None:
        print(f"\033[{self.exit.y * 2};{self.exit.x * 3 - 1}H", end="")
        print(f"{Color.MAGENTA.value}{Color.BOLD.value}{self.exit_icon}{Color.RESET.value}", end="")



# self.grid[line*2+1][col*3+1] = -1
# self.grid[line*2+1][col*3+2] = -1