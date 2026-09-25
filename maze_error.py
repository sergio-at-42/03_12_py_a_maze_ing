class MazeError(Exception):
    """Base class for maze related errors."""

class EntryIn42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Entry point in 42 ! Very Bad")

class ExitIn42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Exit point in 42 ! Very Bad")

class WithToSmallFor42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("With to small for 42 ! Very Bad")

class HeightToSmallFor42Error(MazeError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Height to small for 42 ! Very Bad")
