from enum import Enum


class WallType(Enum):

    # ░
    UNIQ01 = "░"

    # ▒
    UNIQ02 = "▒"

    # ▓
    UNIQ03 = "▓"

    # █
    UNIQ04 = "█"

    # #
    HASHTAG = "#"

    # @
    AT = "@"

    # ┌─┬┐ ─
    # ├─┼┤ │
    # └─┴┘
    SIMPLE = "simple"

    # ╔═╦╗ ═
    # ╠═╬╣ ║
    # ╚═╩╝
    DOUBLE = "double"

    # ░ ▒ ▓ █

    # ┌─┬┐ ─
    # ├─┼┤ │
    # └─┴┘

    # ╔═╦╗ ═
    # ╠═╬╣ ║
    # ╚═╩╝
