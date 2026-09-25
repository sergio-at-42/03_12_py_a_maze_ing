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


class WidthToSmallFor42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Width to small for 42 ! Very Bad")


class HeightToSmallFor42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Height to small for 42 ! Very Bad")
