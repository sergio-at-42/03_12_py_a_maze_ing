from random import randint
import sys, termios, tty

from .maze import Maze
from .wall import Wall
from .color import Color
from .wall_type import WallType


class MazeMenu():

    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze
        self.error_text: str = ""

    def menu_choice(self, choice: str) -> bool:
        stay_in_loop: bool = True
        match choice:
            case "Q":
                self.maze.config.wall_color = Color.BLACK
            case "W":
                self.maze.config.wall_color = Color.RED
            case "E":
                self.maze.config.wall_color = Color.GREEN
            case "R":
                self.maze.config.wall_color = Color.YELLOW
            case "T":
                self.maze.config.wall_color = Color.BLUE
            case "Y":
                self.maze.config.wall_color = Color.MAGENTA
            case "U":
                self.maze.config.wall_color = Color.CYAN
            case "I":
                self.maze.config.wall_color = Color.WHITE
            case "A":
                self.maze.config.wall_bkcolor = Color.BG_BLACK
            case "S":
                self.maze.config.wall_bkcolor = Color.BG_RED
            case "D":
                self.maze.config.wall_bkcolor = Color.BG_GREEN
            case "F":
                self.maze.config.wall_bkcolor = Color.BG_YELLOW
            case "G":
                self.maze.config.wall_bkcolor = Color.BG_BLUE
            case "H":
                self.maze.config.wall_bkcolor = Color.BG_MAGENTA
            case "J":
                self.maze.config.wall_bkcolor = Color.BG_CYAN
            case "K":
                self.maze.config.wall_bkcolor = Color.BG_WHITE
            case "1":
                self.maze.config.wall_type = WallType.UNIQ01
            case "2":
                self.maze.config.wall_type = WallType.UNIQ02
            case "3":
                self.maze.config.wall_type = WallType.UNIQ03
            case "4":
                self.maze.config.wall_type = WallType.UNIQ04
            case "5":
                self.maze.config.wall_type = WallType.HASHTAG
            case "6":
                self.maze.config.wall_type = WallType.AT
            case "7":
                self.maze.config.wall_type = WallType.SIMPLE
            case "8":
                self.maze.config.wall_type = WallType.DOUBLE
            case "N":
                self.maze.path.visible = True
                self.maze.path.speed = 10
            case "M":
                self.maze.path.visible = False
            case "B":
                self.maze.generator.seed = randint(0, 32767)
                self.maze.new_maze()
            case "Z":
                self.maze.write_output_file()
            case "X":
                stay_in_loop = False
        return (stay_in_loop)

    def input_loop(self) -> None:
        stay_in_loop: bool = True
        while stay_in_loop:
            self.maze.display()
            self.display()
            stay_in_loop = self.menu_choice(self.input_one_key().upper())

    def display(self) -> None:

        # Frame top
        print(f"\033[{self.maze.config.height*2+2};1H", end="")
        print("")
        print(f"{self.maze.config.wall_color.value}{self.maze.config.wall_bkcolor.value}{Color.BOLD.value}", end="")
        print(f"╔{"═" * 79}╗", end="")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

        # Wall color
        self.display_frame_side()
        print(f"{self.maze.config.wall_color.value}{self.maze.config.wall_bkcolor.value}{Color.BOLD.value}      WALL COLOR       ", end="")
        print(f"{Color.BG_BLACK.value}{Color.BOLD.value}  <Q>  ", end="")
        print(f"{Color.BG_RED.value}{Color.BOLD.value}  <W>  ", end="")
        print(f"{Color.BG_GREEN.value}{Color.BOLD.value}  <E>  ", end="")
        print(f"{Color.BG_YELLOW.value}{Color.BOLD.value}  <R>  ", end="")
        print(f"{Color.BG_BLUE.value}{Color.BOLD.value}  <T>  ", end="")
        print(f"{Color.BG_MAGENTA.value}{Color.BOLD.value}  <Y>  ", end="")
        print(f"{Color.BG_CYAN.value}{Color.BOLD.value}  <U>  ", end="")
        print(f"{Color.BG_WHITE.value}{Color.BOLD.value}  <I>  ", end="")
        self.display_frame_side()
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

        # Background color
        self.display_frame_side()
        print(f"{self.maze.config.wall_color.value}{self.maze.config.wall_bkcolor.value}{Color.BOLD.value} WALL BACKGROUND COLOR ", end="")
        print(f"{Color.BG_BLACK.value}{Color.BOLD.value}  <A>  ", end="")
        print(f"{Color.BG_RED.value}{Color.BOLD.value}  <S>  ", end="")
        print(f"{Color.BG_GREEN.value}{Color.BOLD.value}  <D>  ", end="")
        print(f"{Color.BG_YELLOW.value}{Color.BOLD.value}  <F>  ", end="")
        print(f"{Color.BG_BLUE.value}{Color.BOLD.value}  <G>  ", end="")
        print(f"{Color.BG_MAGENTA.value}{Color.BOLD.value}  <H>  ", end="")
        print(f"{Color.BG_CYAN.value}{Color.BOLD.value}  <J>  ", end="")
        print(f"{Color.BG_WHITE.value}{Color.BOLD.value}  <K>  ", end="")
        self.display_frame_side()
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

        # Wall type
        self.display_frame_side()
        print(f"{self.maze.config.wall_color.value}{self.maze.config.wall_bkcolor.value}{Color.BOLD.value}       WALL TYPE       ", end="")
        print(f" ░<1>░ ", end="")
        print(f" ▒<2>▒ ", end="")
        print(f" ▓<3>▓ ", end="")
        print(f" █<4>█ ", end="")
        print(f" #<5># ", end="")
        print(f" @<6>@ ", end="")
        print(f" ┼<7>┼ ", end="")
        print(f" ╬<8>╬ ", end="")
        self.display_frame_side()
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

        # Display path
        self.display_frame_side()
        print(f"{self.maze.config.wall_color.value}{self.maze.config.wall_bkcolor.value}{Color.BOLD.value}     DISPLAY PATH      ", end="")
        print(f"       <N> SHOW PATH        ", end="")
        print(f"       <M> HIDE PATH        ", end="")
        self.display_frame_side()
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

        # Exit
        self.display_frame_side()
        print(f"{self.maze.config.wall_color.value}{self.maze.config.wall_bkcolor.value}{Color.BOLD.value}     SAVE & EXIT       ", end="")
        print(f"   <B> NEW MAZE   ", end="")
        print(f"   <Z> SAVE MAZE   ", end="")
        print(f"    <X> TO EXIT    ", end="")
        self.display_frame_side()
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

        # Frame bottom
        print(f"{self.maze.config.wall_color.value}{self.maze.config.wall_bkcolor.value}{Color.BOLD.value}", end="")
        print(f"╚{"═" * 79}╝", end="")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")

        # Error
        self.display_error() if len(self.error_text) else self.hide_error()

    def display_frame_side(self) -> None:
        print(f"{self.maze.config.wall_color.value}{self.maze.config.wall_bkcolor.value}{Color.BOLD.value}", end="")
        print("║", end="")

    def input_one_key(self) -> str:
        key: str = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return (key)

    def display_error(self) -> None:
        print(f"{Color.RED.value}{Color.BLINKING.value}{Color.BOLD.value}", end="")
        print(f"{self.error_text}", end="")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")
        self.error_text = ""

    def hide_error(self) -> None:
        print(f"{" " * len(self.error_text)}", end="")
        print(f"{Color.RESET.value}{Color.CURSOR_OFF.value}")
