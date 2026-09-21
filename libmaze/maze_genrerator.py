import random

from .maze_config import MazeConfig


N, E, S, W = 1, 2, 4, 8
OPPOSITE = {N: S, S: N, E: W, W: E}
DELTA = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
PATTERN_42 = [
    "X..X.XXXX",
    "X..X....X",
    "XXXX.XXXX",
    "...X.X...",
    "...X.XXXX",
]
PATTERN_W = len(PATTERN_42[0])   # 9
PATTERN_H = len(PATTERN_42)     # 5

# dans maze ou dans main il faut mettre
# generator = MazeGenerator(
#     width=config.width,
#     height=config.height,
#     entry=(config.entry.x, config.entry.y),
#     exit=(config.exit.x, config.exit.y),
#     seed=config.seed,
#     perfect=config.perfect,
# )
class MazeGenerator:
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int], seed: int = 0, perfect: bool = True,) -> None:
    # def __init__(self, maze_config: MazeConfig) -> None:
    #     self.maze_config: MazeConfig = maze_config
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        # grid representation of the maze, where each cell is represented by a
        # 4-bit integer
        self.grid: list[list[int]] = [
            [0b1111 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self._solution_path: list[tuple[int, int]] = []


    def check_neighbors(
        self, x: int, y: int, visited: list[list[bool]],
        reserved: set[tuple[int, int]]
    ) -> list[tuple[int, int, int]]:
        """ Return tuple of valid and unvisited neighbors of (x, y).
        Each element is (direction, nx, ny)."""

        result: list[tuple[int, int, int]] = []
        for direction, (dx, dy) in DELTA.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if visited[ny][nx] or (nx, ny) in reserved:
                continue
            result.append((direction, nx, ny))
        return result


    def brick_walls(self, x: int, y: int,
                    direction: int, nx: int, ny: int) -> None:
        """brick the wall between (x, y) and its neighbor (nx, ny)
        in the given direction, on both sides (consistency guaranteed)."""

        self.grid[y][x] &= ~direction
        self.grid[ny][nx] &= ~OPPOSITE[direction]


    def set_pattern(self) -> set[tuple[int, int]]:
        """ set the coordinates of the '42' pattern.
        Returns the set of reserved cells (empty if the maze is too small,
        with error message displayed)."""

        margin = 2  # on garde au moins 2 cellules de marge autour du motif
        if self.width < PATTERN_W + margin or self.height < PATTERN_H + margin:
            print(
                "Warning: maze too small to display the '42' pattern "
                f"(needs at least {PATTERN_W + margin}x{PATTERN_H + margin})."
            )
            return set()

        offset_x = (self.width - PATTERN_W) // 2
        offset_y = (self.height - PATTERN_H) // 2

        reserved: set[tuple[int, int]] = set()
        for row, line in enumerate(PATTERN_42):
            for col, char in enumerate(line):
                if char == "X":
                    reserved.add((offset_x + col, offset_y + row))
        return reserved


    def dfs(self) -> None:
        """ Depth-first search to generate the maze """
        visited = [[False] * self.width for _ in range(self.height)]
        start = self.entry
        stack: list[tuple[int, int]] = [start]
        visited[start[1]][start[0]] = True

        while stack:
            x, y = stack[-1]
            neighbors = self.check_neighbors(x, y, visited, self.reserved)
            if not neighbors:
                stack.pop()
                continue
            direction, nx, ny = self.rng.choice(neighbors)
            self.brick_walls(x, y, direction, nx, ny)
            visited[ny][nx] = True
            stack.append((nx, ny))
            
    def generate(self) -> None:
        self.rng = random.Random(self.seed)
        self.reserved = self.set_pattern()
        entry_xy = self.entry
        exit_xy = self.exit
        if entry_xy in self.reserved or exit_xy in self.reserved:
            raise ValueError(
                "Entry or exit coordinates fall inside the '42' pattern; "
                "adjust the maze size or entry/exit coordinates."
            )
        self.dfs()
        # if not self.perfect:
        #     self.braid()









    # def  pacman_mode(self) -> None:
# 4 coins + centre = corridors ouverts
# Au moins 2 routes indépendantes (donc au moins 2 boucles, pas juste une)
# Dead-ends rares, idéalement zéro
# Toujours respecter la contrainte largeur ≤ 2 cellules (déjà valable pour le DFS pur, mais il faut la revalider après ajout de boucles)


    # def braid()->None :
# Compter les voisins accessibles en testant chaque direction avec cell & jdirection == 0 — plus explicite et réutilise directement N,E,S,W
# create a CellStack (LIFO) to hold a list of cell locations 
# set TotalCells = number of cells in grid 
# choose a cell at random and call it CurrentCell 
# set VisitedCells = 1 
  
# while VisitedCells < TotalCells 

#     find all neighbors of CurrentCell with all walls intact  
#     if one or more found 
#         choose one at random 
#         knock down the wall between it and CurrentCell 
#         push CurrentCell location on the CellStack 
#         make the new cell CurrentCell 
#         add 1 to VisitedCells else 
#         pop the most recent cell entry off the CellStack 
#         make it CurrentCell endIf 

# endWhile