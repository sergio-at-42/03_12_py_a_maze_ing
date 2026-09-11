from typing import Any, Self

from libmaze import MazeConfig, Color


class Maze:

    def __init__(self) -> None:
        self.config: MazeConfig = MazeConfig()
