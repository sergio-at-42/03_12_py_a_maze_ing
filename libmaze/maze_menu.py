from typing import Any, Self

from .maze import Maze
from .wall import Wall
from .coord import Coord
from .color import Color


class MazeMenu:

    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze

    def display(self) -> None:

        # Wall color
        print(f"\033[{self.maze.config.height*2+2};1H", end="")
        print(f"{Color.BG_BLUE.value}{Color.YELLOW.value}{Color.BOLD.value}      WALL COLOR      ", end="")
        print(f"{Color.BG_BLACK.value}{Color.BOLD.value}  <Q>  ", end="")
        print(f"{Color.BG_RED.value}{Color.BOLD.value}  <W>  ", end="")
        print(f"{Color.BG_GREEN.value}{Color.BOLD.value}  <E>  ", end="")
        print(f"{Color.BG_YELLOW.value}{Color.BOLD.value}  <R>  ", end="")
        print(f"{Color.BG_BLUE.value}{Color.BOLD.value}  <T>  ", end="")
        print(f"{Color.BG_MAGENTA.value}{Color.BOLD.value}  <Y>  ", end="")
        print(f"{Color.BG_CYAN.value}{Color.BOLD.value}  <U>  ", end="")
        print(f"{Color.BG_WHITE.value}{Color.BOLD.value}  <I>  ", end="")
        print(f"{Color.RESET.value}")

        # Background color
        print(f"{Color.BOLD.value}   BACKGROUND COLOR   ", end="")
        print(f"{Color.BG_BLACK.value}{Color.BOLD.value}  <A>  ", end="")
        print(f"{Color.BG_RED.value}{Color.BOLD.value}  <S>  ", end="")
        print(f"{Color.BG_GREEN.value}{Color.BOLD.value}  <D>  ", end="")
        print(f"{Color.BG_YELLOW.value}{Color.BOLD.value}  <F>  ", end="")
        print(f"{Color.BG_BLUE.value}{Color.BOLD.value}  <G>  ", end="")
        print(f"{Color.BG_MAGENTA.value}{Color.BOLD.value}  <H>  ", end="")
        print(f"{Color.BG_CYAN.value}{Color.BOLD.value}  <J>  ", end="")
        print(f"{Color.BG_WHITE.value}{Color.BOLD.value}  <K>  ", end="")
        print(f"{Color.RESET.value}")
                 
        # for line in range(self.config.height*2+1):
        #     for col in range(self.config.width*2+1):
        #         print(self.construct_wall(line, col), end="")
        #     print()
        # print(f"\033[{self.config.entry.y};{self.config.entry.x}H", end="")
        # print(f"{Color.RED.value}{Color.BOLD.value}{self.config.entry_icon}{Color.RESET.value}", end="")
        # print(f"\033[{self.config.exit.y};{self.config.exit.x}H", end="")
        # print(f"{Color.MAGENTA.value}{Color.BOLD.value}{self.config.exit_icon}{Color.RESET.value}", end="")