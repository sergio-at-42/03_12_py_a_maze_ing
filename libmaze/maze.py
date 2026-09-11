from typing import Any, Self

from .maze_config import MazeConfig


class Maze:

    def __init__(self) -> None:
        self.config: MazeConfig = MazeConfig()
