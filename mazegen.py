import random
from collections import deque
"""mazegen — reusable maze generation and solving library.

Generates a maze on a rectangular grid using a depth-first search
(recursive backtracker). Two modes are available:

- perfect=True  : a spanning tree — exactly one path between any two cells,
  no loops.
- perfect=False (default): a "Pac-Man"-style playable board — fully
  connected, corners and centre open, at least two independent loops,
  very few (or no) dead-ends, and no corridor wider than 2 cells.

Basic usage
-----------
    from mazegen import MazeGenerator

    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        seed=42,       # optional, defaults to 0 — reproducible generation
        perfect=False, # optional, defaults to True
    )
    generator.generate()

Accessing the generated structure
----------------------------------
Each cell is stored as a 4-bit integer in generator.grid[y][x], where a
set bit means the wall on that side is CLOSED:
    bit 0 (1) = North   bit 1 (2) = East
    bit 2 (4) = South   bit 3 (8) = West

    is_closed = generator.is_wall(x, y, direction)
    is_open   = generator.is_open(x, y, direction)

To get the whole maze as hexadecimal rows (one digit per cell, matching
the subject's output format):
    rows = generator.to_hexa_rows()

Accessing a solution
---------------------
    path = generator.solve()          # list of "N"/"E"/"S"/"W" letters
    # or, to reuse the last computed solution without recomputing:
    path = generator.solution_path

Custom parameters
------------------
- width, height : int, grid dimensions (in cells)
- entry, exit   : tuple[int, int], (x, y) coordinates
- seed          : int, controls reproducibility — same seed + same
                  parameters always produce the same maze
- perfect       : bool, see the two modes above
"""

N, E, S, W = 1, 2, 4, 8
OPPOSITE = {N: S, S: N, E: W, W: E}
DELTA = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
DIRECTION_LETTER = {N: "N", E: "E", S: "S", W: "W"}
PATTERN_42 = [
    "X..X.XXXX",
    "X..X....X",
    "XXXX.XXXX",
    "...X.X...",
    "...X.XXXX",
]
PATTERN_W = len(PATTERN_42[0])   # 9
PATTERN_H = len(PATTERN_42)     # 5


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int], seed: int = 0,
                 perfect: bool = True,) -> None:
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
        self._solution_path: list[str] = []

    def init_grid(self) -> None:
        self.grid = [[0b1111 for _ in range(self.width)]
                     for _ in range(self.height)]
###
# depth-first search maze generation

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

    def restore_wall(self, x: int, y: int,
                     direction: int, nx: int, ny: int) -> None:
        """ Put the wall back between two neighboring cells."""
        self.grid[y][x] |= direction
        self.grid[ny][nx] |= OPPOSITE[direction]

    def is_wall(self, x: int, y: int, direction: int) -> bool:
        """Return True if the given wall exists."""
        return (self.grid[y][x] & direction) != 0

    def is_open(self, x: int, y: int, direction: int) -> bool:
        """Return True if there is no wall in this direction."""
        return (self.grid[y][x] & direction) == 0

    def set_pattern(self) -> set[tuple[int, int]]:
        """Set the coordinates of the '42' pattern.
        The X cells are reserved and must remain completely closed.
        Returns: Set of reserved coordinates (empty if the maze is too small,
        with error message displayed)."""

        margin = 2  # on garde au moins 2 cellules de marge autour du motif
        if self.width < PATTERN_W + margin or self.height < PATTERN_H + margin:
            raise Exception("Warning: maze too small to display the '42' "
                            "pattern (needs at least"
                            f"{PATTERN_W + margin}x{PATTERN_H + margin}).")

        offset_x = (self.width - PATTERN_W) // 2
        offset_y = (self.height - PATTERN_H) // 2

        reserved: set[tuple[int, int]] = set()
        for row, line in enumerate(PATTERN_42):
            for col, char in enumerate(line):
                if char == "X":
                    reserved.add((offset_x + col, offset_y + row))
        return reserved

    def dfs(self) -> None:
        """ Depth-first search to generate the maze
         The resulting maze is a spanning tree:
        - every playable cell is reachable
        - there are no loops
        - there is exactly one path between any two cells """

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

###
#  Methods for maze analysis and modification

    def degree(self, x: int, y: int) -> int:
        """ Return the number of open connections of a cell.
        0 = isolated
        1 = dead end
        2 = corridor
        3 = junction
        4 = open intersection """

        if (x, y) in self.reserved:
            return 0
        degree = 0

        for direction, (dx, dy) in DELTA.items():
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if (nx, ny) in self.reserved:
                continue
            if self.is_open(x, y, direction):
                degree += 1
        return degree

    def count_dead_ends(self) -> int:
        """Count playable cells having exactly one open connection."""
        count = 0

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.reserved:
                    continue
                if self.degree(x, y) == 1:
                    count += 1
        return count

    def count_playable_cells(self) -> int:
        """Return the number of non-reserved cells."""
        return (self.width * self.height - len(self.reserved))

    def count_edges(self) -> int:
        """Count open connections.
        Each edge is counted only once:
        - East
        - South """
        edges = 0
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.reserved:
                    continue
                # East connection.
                if x + 1 < self.width:
                    if (x + 1, y) not in self.reserved:
                        if self.is_open(x, y, E):
                            edges += 1
                # South connection.
                if y + 1 < self.height:
                    if (x, y + 1) not in self.reserved:
                        if self.is_open(x, y, S):
                            edges += 1
        return edges

    def count_loops(self) -> int:
        """ Number of independent cycles in the connected maze.
        For a connected graph: loops = edges - vertices + 1 """
        vertices = self.count_playable_cells()
        edges = self.count_edges()
        if vertices == 0:
            return 0
        return edges - vertices + 1

    def is_open_3x3area(self, start_x: int, start_y: int) -> bool:
        """Return True if the 3x3 area starting at (start_x, start_y) is
        completely open.
        A 2x3 or 3x2 area is allowed."""
        # The 3x3 block must fit inside the maze.
        if start_x < 0 or start_y < 0:
            return False

        if start_x + 2 >= self.width:
            return False

        if start_y + 2 >= self.height:
            return False
        # If any reserved cell is inside the 3x3,
        # it cannot be a completely open area.
        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 3):
                if (x, y) in self.reserved:
                    return False

        # Check the 6 horizontal connections.
        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 2):
                if not self.is_open(x, y, E):
                    return False

        # Check the 6 vertical connections.
        for y in range(start_y, start_y + 2):
            for x in range(start_x, start_x + 3):
                if not self.is_open(x, y, S):
                    return False
        return True

    def creates_open_3x3area(self, x: int, y: int, nx: int, ny: int) -> bool:
        """ Check all possible 3x3 blocks that could contain either
        endpoint of a newly opened connection."""
        # We only need to check 3x3 blocks around the two cells
        # whose connection was changed.
        cells = [(x, y), (nx, ny)]
        checked: set[tuple[int, int]] = set()
        for cx, cy in cells:
            for start_x in range(cx - 2, cx + 1):
                for start_y in range(cy - 2, cy + 1):
                    if (start_x, start_y) in checked:
                        continue

                    checked.add((start_x, start_y))
                    if self.is_open_3x3area(start_x, start_y):
                        return True
        return False

    def can_open_wall(self, x: int, y: int,
                      direction: int, nx: int, ny: int) -> bool:
        """ Try to open a wall.
        The wall is actually opened if the operation is valid.
        Returns:
            True  -> wall was safely opened
            False -> wall was not opened"""

        # Coordinates must be valid.
        if not (
            0 <= x < self.width
            and 0 <= y < self.height
            and 0 <= nx < self.width
            and 0 <= ny < self.height
        ):
            return False

        # Never touch the 42.
        if (x, y) in self.reserved:
            return False

        if (nx, ny) in self.reserved:
            return False

        # The two cells must actually be neighbors.
        dx = nx - x
        dy = ny - y

        expected_delta = DELTA[direction]

        if (dx, dy) != expected_delta:
            return False
        # There must currently be a wall.
        if not self.is_wall(x, y, direction):
            return False

        # Temporarily remove the wall.
        self.brick_walls(x, y, direction, nx, ny)

        # Check whether this created a forbidden 3x3.
        if self.creates_open_3x3area(x, y, nx, ny):
            # Undo.
            self.restore_wall(x, y, direction, nx, ny)
            return False
        # Keep the wall open.
        return True

    def get_closed_internal_walls(self) -> list[tuple[int,
                                                      int, int, int, int]]:
        """ Return all currently closed internal walls.
        Each item is: (x, y, direction, nx, ny)
        We only consider East and South so that each wall appears once."""

        walls: list[tuple[int, int, int, int, int]] = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.reserved:
                    continue

                if x + 1 < self.width:
                    nx = x + 1
                    ny = y
                    if (nx, ny) not in self.reserved:
                        if self.is_wall(x, y, E):
                            walls.append((x, y, E, nx, ny))

                if y + 1 < self.height:
                    nx = x
                    ny = y + 1

                    if (nx, ny) not in self.reserved:

                        if self.is_wall(x, y, S):

                            walls.append((x, y, S, nx, ny))

        return walls

    def corner_positions(self) -> list[tuple[int, int]]:
        """Return the four corners."""
        return [(0, 0), (
            self.width - 1, 0), (
                0, self.height - 1), (self.width - 1, self.height - 1)
            ]

    def get_closed_neighbors(self, x: int, y: int) -> list[tuple[int,
                                                                 int, int]]:
        """ Return closed internal walls around a cell.
        Each result is: (direction, nx, ny)"""

        result: list[tuple[int, int, int]] = []

        for direction, (dx, dy) in DELTA.items():

            nx = x + dx
            ny = y + dy

            # Outside = external border.
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            if (nx, ny) in self.reserved:
                continue

            if (x, y) in self.reserved:
                continue

            # Only consider walls that are still closed.
            if self.is_wall(x, y, direction):
                result.append(
                    (direction, nx, ny))
        return result

###
# Mode pac-man: open corners, open center, reduce dead ends, add loops

    def open_corners(self) -> None:
        """ Make the four corners proper open corridors.
        A corner has only two possible internal neighbors,
        therefore degree 2 is the ideal state."""

        for x, y in self.corner_positions():
            if (x, y) in self.reserved:
                continue
            neighbors = self.get_closed_neighbors(x, y)
            self.rng.shuffle(neighbors)

            for direction, nx, ny in neighbors:
                if self.degree(x, y) >= 2:
                    break

                self.can_open_wall(x, y, direction, nx, ny)

    def center(self) -> tuple[int, int]:
        """Return the center cell.
        For even dimensions this selects the lower/right cell."""

        return (self.width // 2, self.height // 2)

    def open_center(self) -> None:
        """Ensure the center is an actual corridor. We require at least two
        connections."""

        cx, cy = self.center()
        if (cx, cy) in self.reserved:
            return

    def dead_end_cells(self) -> list[tuple[int, int]]:
        """Return all current dead-end cells."""
        result: list[tuple[int, int]] = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.reserved:
                    continue
                if self.degree(x, y) == 1:
                    result.append((x, y))

        return result

    def reduce_dead_ends(self, max_dead_ends: int = 2) -> None:
        """ Try to reduce the number of dead ends.
        We preferentially open a wall adjacent to a dead end.
        We stop when:
            dead_ends <= max_dead_ends
        or when no safe wall can be opened anymore.
        """

        # Prevent infinite loops.
        max_iterations = (self.width * self.height * 4)
        iterations = 0
        while (self.count_dead_ends() > max_dead_ends and
               iterations < max_iterations):
            iterations += 1
            dead_ends = self.dead_end_cells()
            if not dead_ends:
                break
            self.rng.shuffle(dead_ends)

            opened = False
            for x, y in dead_ends:
                neighbors = self.get_closed_neighbors(x, y)
                self.rng.shuffle(neighbors)

                for direction, nx, ny in neighbors:
                    if self.can_open_wall(x, y, direction, nx, ny):
                        opened = True
                        break
                if opened:
                    break
            if not opened:
                break

    def add_loops(self, minimum_loops: int = 2) -> None:
        """Add additional connections until the maze contains at least
        `minimum_loops` independent loops.
        This is done by randomly opening walls,
        while ensuring that no 3x3 area becomes completely open.
        """
        if self.count_loops() >= minimum_loops:
            return

        walls = self.get_closed_internal_walls()
        self.rng.shuffle(walls)

        for x, y, direction, nx, ny in walls:
            if self.count_loops() >= minimum_loops:
                return
            self.can_open_wall(x, y, direction, nx, ny)
        if self.count_loops() < minimum_loops:
            raise ValueError(
                f"Could not create {minimum_loops} loops without creating"
                "a forbidden 3x3 open area."
            )

    def make_non_perfect(self) -> None:
        target_loops = 2
        target_dead_ends = 2
        # First eliminate dead ends.
        self.reduce_dead_ends(target_dead_ends)
        # Then guarantee at least two loops
        self.add_loops(target_loops)

    def generate_non_perfect(self) -> None:
        """
        Generate a Pac-Man-like non-perfect maze.
        """
        self.dfs()
        self.open_corners()
        self.open_center()
        self.make_non_perfect()

###
# validation and generation entry points

    def validate(self) -> None:
        if not (0 <= self.entry[0] < self.width
                and 0 <= self.entry[1] < self.height):
            raise ValueError("Entry is outside the maze.")
        if not (0 <= self.exit[0] < self.width
                and 0 <= self.exit[1] < self.height):
            raise ValueError("Exit is outside the maze.")
        if self.entry == self.exit:
            raise ValueError("Entry and exit must be different.")
        if self.entry in self.reserved:
            raise ValueError("Entry is inside the 42 pattern.")
        if self.exit in self.reserved:
            raise ValueError("Exit is inside the 42 pattern.")

    def generate(self) -> None:
        """Generate the maze."""
        self.init_grid()
        self.rng = random.Random(self.seed)
        self.reserved = self.set_pattern()
        self.validate()
        self._solution_path = []
        if self.perfect:
            self.dfs()
        else:
            self.generate_non_perfect()

###
# solve method using bfs
    def solve(self) -> list[str]:
        """ Solve the maze using breadth-first search."""
        start = self.entry
        end = self.exit
        visited = {start}
        parent: dict[tuple[int, int], tuple[tuple[int, int], int]] = {}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            if current == end:
                break
            x, y = current
            for direction in (N, E, S, W):
                if not self.is_open(x, y, direction):
                    continue
                dx, dy = DELTA[direction]
                neighbor = (x + dx, y + dy)
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                parent[neighbor] = (current, direction)
                queue.append(neighbor)
        else:
            raise ValueError("No path found between entry and exit.")

        path: list[str] = []
        cell = end
        while cell != start:
            prev, direction = parent[cell]
            path.append(DIRECTION_LETTER[direction])
            cell = prev
        path.reverse()
        self._solution_path = path
        return path

    @property
    def solution_path(self) -> list[str]:
        """Access the solution path. If it has not been computed yet,
        compute it."""
        if not self._solution_path:
            self.solve()
        return self._solution_path
