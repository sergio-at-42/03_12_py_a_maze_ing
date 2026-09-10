from typing import Any, Self

from .maze_config import MazeConfig


class Maze:

    def __init__(self, config_file_name: str) -> None:
        self.config: MazeConfig = MazeConfig()
