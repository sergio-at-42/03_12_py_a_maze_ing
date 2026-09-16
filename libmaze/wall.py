from typing import Any, Self

from .color import Color
from .wall_type import WallType
from .coord import Coord


class Wall():

    def __init__(self, type: WallType, color: Color, bkcolor: Color):
        self.type: WallType = WallType.SIMPLE    # SIMPLE DOUBLE UNIQ01 UNIQ02 UNIQ03 UNIQ04 HASHTAG AT
        self.color: Color = Color.YELLOW
        self.bkcolor: Color = Color.BG_BLUE
        self.element: list[str] = [" "] * 17
        self.init_wall(type, color, bkcolor)

    def init_wall(self, type: WallType, color: Color, bkcolor: Color) -> None:

        self.type = type
        self.color = color
        self.bkcolor = bkcolor

        match self.type:

            case WallType.SIMPLE:
                self.element[0] = "┼"
                self.element[1] = "│"
                self.element[2] = "─"
                self.element[3] = "└"
                self.element[4] = "│"
                self.element[5] = "│"
                self.element[6] = "┌"
                self.element[7] = "├"
                self.element[8] = "─"
                self.element[9] = "┘"
                self.element[10] = "─"
                self.element[11] = "┴"
                self.element[12] = "┐"
                self.element[13] = "┤"
                self.element[14] = "┬"
                self.element[15] = "┼"

            case WallType.DOUBLE:
                self.element[0] = "╬"
                self.element[1] = "║"
                self.element[2] = "═"
                self.element[3] = "╚"
                self.element[4] = "║"
                self.element[5] = "║"
                self.element[6] = "╔"
                self.element[7] = "╠"
                self.element[8] = "═"
                self.element[9] = "╝"
                self.element[10] = "═"
                self.element[11] = "╩"
                self.element[12] = "╗"
                self.element[13] = "╣"
                self.element[14] = "╦"
                self.element[15] = "╬"

            case _:
                self.element[0] = self.type.value

        self.element[16] = self.element[0]

    def construct(self, element: int) -> str:
        block = False
        if element == -1:
            block = True
            element = 16
        if self.type != WallType.SIMPLE and self.type != WallType.DOUBLE:
            element = 0
        wall_element = f"{self.color.value}{self.bkcolor.value}{Color.INVERSION.value if block else ""}{Color.BLINKING.value if block else ""}{self.element[element]}{Color.RESET.value}"
        return (wall_element)

# ╔═╦╗ ┌─┬┐ ═ ─
# ╠═╬╣ ├─┼┤ ║ │
# ╚═╩╝ └─┴┘ ▒ ░