import square
import random


class Grid(object):
    """Grid is the playable minefield which consists of squares."""

    def __init__(self, size_x, size_y, mines):
        super(Grid, self).__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.mines = mines
        self.squares = [[None for x in range(size_x)] for y in range(size_y)]
        self.emptyfill()
        self.minefill()
        self.numberfill()
        self.revealed_count = 0
        self.nonmines = (size_x * size_y) - mines

    def get_square(self, x, y):
        """Returns the square at specified coords x, y.
        Use this method if you need to access squares from outside the class.
        """

        return self.squares[y][x]

    def reveal_sq(self, x, y):
        """Reveal a square and increase revealed counter."""

        if not self.get_square(x, y).revealed:
            self.revealed_count += 1
        self.squares[y][x].reveal()

    def get_size(self):
        return self.size_x * self.size_y

    def emptyfill(self):
        """Fill the whole grid with empty squares."""

        for y in range(self.size_y):
            for x in range(self.size_x):
                self.squares[y][x] = square.Empty(x, y)

    def minefill(self):
        """Add specified amount of mine squares
        to random coordinates on the grid."""

        def _rand_coords():
            """Returns random coordinate tuple limited by grid size."""

            return random.randint(0, self.size_x - 1), random.randint(
                0, self.size_y - 1)

        coords = [(None, None) for m in range(self.mines)]

        # Fill coordinate list with unique random coordinate tuples.
        filled = False
        m = 0
        while not filled:
            (x, y) = _rand_coords()
            if (x, y) not in coords:
                coords[m] = x, y
                m += 1
            if m == len(coords):
                filled = True

        # Place bombs on the grid according to coordinate list.
        for y in range(self.size_y):
            for x in range(self.size_x):
                if (x, y) in coords:
                    self.squares[y][x] = square.Bomb(x, y)

    def numberfill(self):
        """Add number squares on to the grid."""

        def _count_adjacent(pos_x, pos_y):
            """Count amount of adjacent bomb squares."""

            adjacent = 0

            for y in range(pos_y - 1, pos_y + 2):
                for x in range(pos_x - 1, pos_x + 2):
                    if y < 0 or x < 0:  # Out of grid.
                        continue
                    if y > len(self.squares) - 1 or x > len(
                            self.squares[0]) - 1:  # Out of grid.
                        continue
                    elif isinstance(self.squares[y][x], square.Bomb):
                        if x != pos_x or y != pos_y:
                            adjacent = adjacent + 1

            return adjacent

        # For each empty square on the grid with adjacent bomb tile(s),
        # replace the empty square with a number square.
        for y in range(self.size_y):
            for x in range(self.size_x):
                count = _count_adjacent(x, y)
                if count > 0 and isinstance(
                        self.squares[y][x], square.Empty):
                    self.squares[y][x] = square.Number(x, y, count)

    def floodfill(self, s_x, s_y):
        """Starting from given coordinates (s_x, s_y)
        reveal all empty and number tiles that are part of a connected area.
        """

        stack_empty = [(s_x, s_y)]  # Coordinates of empty squares.
        stack_number = [(s_x, s_y)]  # Coordinates of number squares.

        while stack_empty:
            xe, ye = stack_empty.pop()
            self.reveal_sq(xe, ye)

            for y in range(ye - 1, ye + 2):
                for x in range(xe - 1, xe + 2):
                    if y < 0 or x < 0:  # Out of grid.
                        continue
                    # Out of grid:
                    elif y > self.size_y - 1 or x > self.size_x - 1:
                        continue
                    elif not self.squares[y][x].revealed:
                        if self.squares[y][x].is_empty():
                            stack_empty.append((x, y))
                        elif self.squares[y][x].is_number():
                            stack_number.append((x, y))

        # Reveal number squares.
        while stack_number:
            xn, yn = stack_number.pop()
            self.reveal_sq(xn, yn)

    def reveal_all(self):
        """Reveals every square on the grid.
        This method is only supposed to be used when the game is over.
        """

        for y in range(self.size_y):
            for x in range(self.size_x):
                # DO NOT USE grid.reveal_sq() here!
                # Instead use square's own reveal -method (square.reveal()).
                # This is to prevent revealed counter from being increased.
                self.squares[y][x].reveal()

    def __str__(self):
        """Returns a human friendly printable string of the grid.
        Iterates through all squares in grid.
        Each square has its own __str__ method,
        which returns the corresponding printable string.
        Also adds row and column numbers to the printable string.
        This method is only viable for grids up to size 100 * 100.
        """

        # Start with some padding.
        s = "   "

        for x in range(self.size_x):
            # Column numbers:
            s += "{}  ".format(x) if x < 10 else "{} ".format(x)
        s += "\n"
        for y in range(self.size_y):
            # Row numbers:
            s += "{} ".format(y) if y < 10 else "{}".format(y)
            for x in range(self.size_x):
                # Actual squares:
                s += "{}".format(self.squares[y][x])
                if x == self.size_x - 1:  # End of row reached.
                    s += "\n"

        return s
