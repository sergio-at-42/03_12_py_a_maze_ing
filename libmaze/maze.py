from typing import Any, Self

from .maze_config import MazeConfig
from .maze_path import MazePath
from mazegen import MazeGenerator
from .wall import Wall
from .coord import Coord
from .color import Color


class Maze():

    def __init__(self) -> None:
        self.config: MazeConfig = MazeConfig()
        self.cell: str
        self.maze_hexa: list[str]
        self.grid: list[list[int]] = [[0]*(self.config.width*3+1) for _ in range(self.config.height*2+1)]
        self.wall: Wall = Wall(self.config.wall_type, self.config.wall_color, self.config.wall_bkcolor)
        self.path: MazePath = MazePath(self.config)
        # self.generator: MazeGenerator = MazeGenerator(self.config)
        # self.generator: MazeGenerator = MazeGenerator(
        #     width = self.config.width,
        #     height = self.config.height,
        #     entry = (self.config.entry.x, self.config.entry.y),
        #     exit = (self.config.exit.x, self.config.exit.y),
        #     seed = self.config.seed,
        #     perfect = self.config.perfect,
        # )
        self.generator: MazeGenerator = MazeGenerator(self.config.width,
            self.config.height,
            (self.config.entry.x, self.config.entry.y),
            (self.config.exit.x, self.config.exit.y),
            self.config.seed,
            self.config.perfect)
        self.new_maze()

    def new_maze(self) -> None:
        for line in range(self.config.height*2+1):
            for col in range(self.config.width*3+1):
                self.grid[line][col] = 0
        self.generator.width = self.config.width
        self.generator.height = self.config.height
        self.generator.entry = (self.config.entry.x, self.config.entry.y)
        self.generator.exit = (self.config.exit.x, self.config.exit.y)
        self.generator.seed = self.config.seed
        self.generator.perfect = self.config.perfect
        self.generator.generate()
        # for line in range(self.config.height):
        #     for col in range(len(self.maze_hexa[line])):
        #         cell = int(self.maze_hexa[line][col], 16)
        for line in range(len(self.generator.grid)):
            for col in range(len(self.generator.grid[line])):
                cell = self.generator.grid[line][col]
                if cell == 15:
                    self.grid[line*2+1][col*3+1] = -1
                    self.grid[line*2+1][col*3+2] = -1
                if cell//8:
                    cell -= 8
                    self.grid[line*2][col*3] = 1
                    self.grid[line*2+1][col*3] = 1
                    self.grid[line*2+2][col*3] = 1
                if cell//4:
                    cell -= 4
                    self.grid[line*2+2][col*3] = 1
                    self.grid[line*2+2][col*3+1] = 1
                    self.grid[line*2+2][col*3+2] = 1
                if cell//2:
                    cell -= 2
                    self.grid[line*2][col*3+3] = 1
                    self.grid[line*2+1][col*3+3] = 1
                    self.grid[line*2+2][col*3+3] = 1
                if cell:
                    self.grid[line*2][col*3] = 1
                    self.grid[line*2][col*3+1] = 1
                    self.grid[line*2][col*3+2] = 1

    def display(self) -> None:
        # self.new_maze()
        self.wall.init_wall(self.config.wall_type, self.config.wall_color, self.config.wall_bkcolor)
        print("\033[H\033[2J", end="")
        for line in range(self.config.height*2+1):
            for col in range(self.config.width*3+1):
                print(self.construct_wall(line, col), end="")
            print()
        if self.config.perfect and self.path.visible:
            self.path.direction = self.generator.solve()
            self.path.display()
            self.path.display_entry()
            self.path.display_exit()

    def construct_wall(self, line: int, col: int) -> str:
        if self.grid[line][col] < 0:
            if self.grid[line][col+1] < 0:
                wall = self.wall.construct(16)
            else:
                wall = ""
        elif self.grid[line][col] == 0:
            wall = " "
        else:
            neightbor: int = 0
            if self.grid[line][col] > 0:
                if line!=0 and self.grid[line-1][col] == 1:
                    neightbor += 1
                if col<self.config.width*3 and self.grid[line][col+1] == 1:
                    neightbor += 2
                if line<self.config.height*2 and self.grid[line+1][col] == 1:
                    neightbor += 4
                if col!=0 and self.grid[line][col-1] == 1:
                    neightbor += 8
            wall = self.wall.construct(neightbor)
        return (wall)
    
    def write_output_file(self) -> bool:
        write_ok: bool = False
        output_line: str = ""
        try:
            with open(self.config.output_file, "w") as output_file:
                output_file.write("# Maze generated with a_maze_ing project\n")
                for line in range(len(self.generator.grid)):
                    # for col in range(len(self.generator.grid[line])):
                    output_line = "".join(format(cell, "X") for cell in self.generator.grid[line])
                        # cell = self.generator.grid[line][col]
                # for line in self.maze_hexa:
                    output_file.write(f"{output_line}\n")
                output_file.write("\n")
                output_file.write("# Entry\n")
                output_file.write(f"{self.config.entry.x},{self.config.entry.y}\n")
                output_file.write("\n")
                output_file.write("# Exit\n")
                output_file.write(f"{self.config.exit.x},{self.config.exit.y}\n")
                output_file.write("\n")
                output_file.write("# Path from Entry to Exit\n")
                output_file.write(f"{self.path.direction}\n")
                write_ok = True
        except Exception as e:
            print(f"{e}")
            write_ok = False
        return (write_ok)



    # def maze_hexa_to_grid(self) -> None:
    #     for line in range(self.config.height):
    #         for col in range(len(self.maze_hexa[line])):
    #             cell = int(self.maze_hexa[line][col], 16)
    #             if cell == 15:
    #                 self.grid[line*2+1][col*2+1] = -1
    #             if cell//8:
    #                 cell -= 8
    #                 self.grid[line*2][col*2] = 1
    #                 self.grid[line*2+1][col*2] = 1
    #                 self.grid[line*2+2][col*2] = 1
    #             if cell//4:
    #                 cell -= 4
    #                 self.grid[line*2+2][col*2] = 1
    #                 self.grid[line*2+2][col*2+1] = 1
    #                 self.grid[line*2+2][col*2+2] = 1
    #             if cell//2:
    #                 cell -= 2
    #                 self.grid[line*2][col*2+2] = 1
    #                 self.grid[line*2+1][col*2+2] = 1
    #                 self.grid[line*2+2][col*2+2] = 1
    #             if cell:
    #                 self.grid[line*2][col*2] = 1
    #                 self.grid[line*2][col*2+1] = 1
    #                 self.grid[line*2][col*2+2] = 1

    # def generate_new(self) -> None:
    #     self.maze_hexa = [
    #         "9515391539551795151151153",
    #         "EBABAE812853C1412BA812812",
    #         "96A8416A84545412AC4282C2A",
    #         "C3A83816A9395384453A82D02",
    #         "96842A852AC07AAD13A8283C2",
    #         "C1296C43AAB83AA92AA8686BA",
    #         "92E853968428444682AC12902",
    #         "AC3814452FA83FFF82C52C42A",
    #         "85684117AFC6857FAC1383D06",
    #         "C53AD043AFFFAFFF856AA8143",
    #         "91441294297FAFD51142C6BAA",
    #         "AA912AC3843FAFFF82856D42A",
    #         "842A8692A92B8517C4451552A",
    #         "816AC384468285293917A9542",
    #         "C416928513C443A828456C3BA",
    #         "91416AA92C393A82801553AAA",
    #         "A81292AA814682C6A8693C6AA",
    #         "A8442C6C2C1168552C16A9542",
    #         "86956951692C1455416928552",
    #         "C545545456545555454444556"
    #     ]

    # def maze_hexa_to_grid(self) -> None:
    #     # for line in range(self.config.height):
    #     #     for col in range(len(self.maze_hexa[line])):
    #     #         cell = int(self.maze_hexa[line][col], 16)
    #     for line in range(len(self.generator.grid)):
    #         for col in range(len(self.generator.grid[line])):
    #             cell = self.generator.grid[line][col]
    #             if cell == 15:
    #                 self.grid[line*2+1][col*3+1] = -1
    #                 self.grid[line*2+1][col*3+2] = -1
    #             if cell//8:
    #                 cell -= 8
    #                 self.grid[line*2][col*3] = 1
    #                 self.grid[line*2+1][col*3] = 1
    #                 self.grid[line*2+2][col*3] = 1
    #             if cell//4:
    #                 cell -= 4
    #                 self.grid[line*2+2][col*3] = 1
    #                 self.grid[line*2+2][col*3+1] = 1
    #                 self.grid[line*2+2][col*3+2] = 1
    #             if cell//2:
    #                 cell -= 2
    #                 self.grid[line*2][col*3+3] = 1
    #                 self.grid[line*2+1][col*3+3] = 1
    #                 self.grid[line*2+2][col*3+3] = 1
    #             if cell:
    #                 self.grid[line*2][col*3] = 1
    #                 self.grid[line*2][col*3+1] = 1
    #                 self.grid[line*2][col*3+2] = 1

