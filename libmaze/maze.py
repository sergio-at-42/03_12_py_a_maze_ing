from .maze_config import MazeConfig
from .maze_path import MazePath
from mazegen import MazeGenerator
from .wall import Wall


class Maze():

    def __init__(self) -> None:
        self.config: MazeConfig = MazeConfig()
        self.cell: str
        self.maze_hexa: list[str]
        self.grid: list[list[int]] = [[0]*(self.config.width*3+1)
                                      for _ in range(self.config.height*2+1)]
        self.wall: Wall = Wall(self.config.wall_type, self.config.wall_color,
                               self.config.wall_bkcolor)
        self.path: MazePath = MazePath(self.config)
        self.generator: MazeGenerator = MazeGenerator(
            self.config.width,
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
        self.config.msg_error_generator = ""
        self.generator.generate()
        self.config.msg_error_generator = f"{self.generator.msg_error}\n"
        self.path.direction = self.generator.solution_path
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
        self.wall.init_wall(
            self.config.wall_type,
            self.config.wall_color,
            self.config.wall_bkcolor)
        print("\033[H\033[2J", end="")
        for line in range(self.config.height*2+1):
            for col in range(self.config.width*3+1):
                print(self.construct_wall(line, col), end="")
            print()
        if self.path.visible:
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
                if line != 0 and self.grid[line - 1][col] == 1:
                    neightbor += 1
                if col < self.config.width * 3 \
                        and self.grid[line][col + 1] == 1:
                    neightbor += 2
                if line < self.config.height * 2 \
                        and self.grid[line + 1][col] == 1:
                    neightbor += 4
                if col != 0 and self.grid[line][col - 1] == 1:
                    neightbor += 8
            wall = self.wall.construct(neightbor)
        return (wall)

    def write_output_file(self) -> bool:
        write_ok: bool = False
        output_line: str = ""
        try:
            with open(self.config.output_file, "w") as output_file:
                # Write Maze
                for line in range(len(self.generator.grid)):
                    output_line = "".join(format(c, "X")
                                          for c in self.generator.grid[line])
                    output_file.write(f"{output_line}\n")
                output_file.write("\n")
                # Write Entry
                output_line = f"{self.config.entry.x},{self.config.entry.y}"
                output_file.write(f"{output_line}\n")
                # Write Exit
                output_line = f"{self.config.exit.x},{self.config.exit.y}"
                output_file.write(f"{output_line}\n")
                # Write Path
                output_line = "".join(direction
                                      for direction in self.path.direction)
                output_file.write(f"{output_line}\n")
                write_ok = True
        except Exception as e:
            print(f"{e}")
            write_ok = False
        return (write_ok)
