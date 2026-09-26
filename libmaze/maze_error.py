class MazeError(Exception):
    """Base class for maze related errors."""


class EntryIn42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Entry is inside the 42 pattern.")


class EntryNotInMaze(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Entry is outside the maze. Auto configurated entry")


class ExitIn42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Exit is inside the 42 pattern.")


class ExitNotInMaze(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Exit is outside the maze. Auto configurated exit")


class ExitegalEntry(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Entry and exit must be different.")


class WidthSmallFor42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Width small for 42, need W=11 ")


class HeightToSmallFor42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Height small for 42, needH=7")


class WidthLessThan0Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Width to small. Must be over 0 !"
                         " Auto configurated width")


class HeightLessThan0Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Height to small. Must be over 0 !"
                         "Auto configurated height")
