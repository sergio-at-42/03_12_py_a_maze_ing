from enum import Enum


class Color(Enum):

    # Reset color
    RESET = "\033[0m"       # Reset
    # Basic colors
    BLACK = "\033[30m"      # Black
    RED = "\033[31m"        # Red
    GREEN = "\033[32m"      # Green
    YELLOW = "\033[33m"     # Yellow
    BLUE = "\033[34m"       # Blue
    MAGENTA = "\033[35m"    # Magenta
    CYAN = "\033[36m"       # Cyan
    WHITE = "\033[37m"      # White
    # Background colors
    BG_BLACK = "\033[40m"   # Black
    BG_RED = "\033[41m"     # Red
    BG_GREEN = "\033[42m"   # Green
    BG_YELLOW = "\033[43m"  # Yellow
    BG_BLUE = "\033[44m"    # Blue
    BG_MAGENTA = "\033[45m" # Magenta
    BG_CYAN = "\033[46m"    # Cyan
    BG_WHITE = "\033[47m"   # White

    BOLD = "\033[1m"	    # Bold
    DIMMED = "\033[2m"	    # Dimmed
    ITALIC = "\033[3m"	    # Italic
    UNDERLINE = "\033[4m"   # Underlined
    BLINKING = "\033[5m"    # Blinking
    INVERSION = "\033[7m"   # Foreground/background inversion
