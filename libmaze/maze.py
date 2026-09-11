from typing import Any, Self

from .maze_config import MazeConfig
from .color import Color


class Maze:

    def __init__(self) -> None:
        self.config: MazeConfig = MazeConfig()
        self.cell: str
        self.maze_hexa: list[str]
        self.grid: list[list[int]] = [[0] * self.config.width * 3 for _ in range(self.config.height * 3)]
        # self.wall: list[str]
        self.generate_new()
        # self.init_wall()

    def maze_hexa_to_grid(self) -> None:
        for line in range(self.config.height):
            for col in range(len(self.maze_hexa[line])):
                cell = int(self.maze_hexa[line][col], 16)
                if cell%8:
                    cell -= 8
                    self.grid[line*3][col*3] += 8
                    self.grid[line*3+1][col*3] = 8
                    self.grid[line*3+2][col*3] += 8
                if cell%4:
                    cell -= 4
                    self.grid[line*3+2][col*3] += 4
                    self.grid[line*3+2][col*3+1] = 4
                    self.grid[line*3+2][col*3+2] += 4
                if cell%2:
                    cell -= 2
                    self.grid[line*3][col*3+2] += 2
                    self.grid[line*3+1][col*3+2] = 2
                    self.grid[line*3+2][col*3+2] += 2
                if cell:
                    self.grid[line*3][col*3] += 1
                    self.grid[line*3][col*3+1] = 1
                    self.grid[line*3][col*3+2] += 1

    def display(self) -> None:
        self.maze_hexa_to_grid()
        for line in range(self.config.height*3):
            for col in range(self.config.width*3):
                # print(self.wall[self.grid[line][col]])
                if self.grid[line][col] > 0:
                    print("▒", end="")
                else:
                    print(" ", end="")
            print()

    def generate_new(self) -> None:
        self.maze_hexa = [
            "9515391539551795151151153",
            "EBABAE812853C1412BA812812",
            "96A8416A84545412AC4282C2A",
            "C3A83816A9395384453A82D02",
            "96842A852AC07AAD13A8283C2",
            "C1296C43AAB83AA92AA8686BA",
            "92E853968428444682AC12902",
            "AC3814452FA83FFF82C52C42A",
            "85684117AFC6857FAC1383D06",
            "C53AD043AFFFAFFF856AA8143",
            "91441294297FAFD51142C6BA",
            "AA912AC3843FAFFF82856D52A",
            "842A8692A92B8517C4451552A",
            "816AC384468285293917A9542",
            "C416928513C443A828456C3BA",
            "91416AA92C393A82801553AAA",
            "A81292AA814682C6A8693C6AA",
            "A8442C6C2C1168552C16A9542",
            "86956951692C1455416928552",
            "C54554545654555545444556"
        ]

    # def init_wall(self) -> None:
    #     self.wall[0] = " "
    #     self.wall[1] = "═"
    #     self.wall[2] = "║"
    #     self.wall[3] = "╗"
    #     self.wall[4] = "═"
    #     self.wall[5] = "═"
    #     self.wall[6] = "╝"
    #     self.wall[7] = ""
    #     self.wall[8] = "║"
    #     self.wall[9] = "╔"
    #     self.wall[10] = "║"
    #     self.wall[11] = ""
    #     self.wall[12] = "╚"
    #     self.wall[13] = ""
    #     self.wall[14] = ""
    #     self.wall[16] = ""

