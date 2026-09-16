from typing import Any, Self
from pydantic import BaseModel, Field, ValidationError, model_validator

from .color import Color
from .wall_type import WallType
from .coord import Coord


class Wall(BaseModel):

    type: WallType = WallType.DOUBLE    # SIMPLE DOUBLE UNIQ01 UNIQ02 UNIQ03 UNIQ04 HASHTAG AT
    color: Color = Color.YELLOW
    bkcolor: Color = Color.BG_BLUE
    element: list[str] = [" "] * 16

    @model_validator(mode='after')
    def init_wall(self) -> "Wall":
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

        return (self)

    def construct(self, element: int) -> str:
        block = False
        if element == -1:
            block = True
            element = 0
        if self.type != WallType.SIMPLE and self.type != WallType.DOUBLE:
            element = 0
        wall_element = f"{self.color.value}{self.bkcolor.value}{Color.INVERSION.value if block else ""}{Color.BLINKING.value if block else ""}{self.element[element]}{Color.RESET.value}"
        return (wall_element)

# ╔═╦╗ ┌─┬┐ ═ ─
# ╠═╬╣ ├─┼┤ ║ │
# ╚═╩╝ └─┴┘ ▒ ░