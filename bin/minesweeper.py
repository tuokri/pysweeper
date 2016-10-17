import time


class Minesweeper(object):
    """Keeps track of game progress."""

    def __init__(self, grid_):
        super(Minesweeper, self).__init__()
        self.grid_ = grid_
        self.lost = False
        self.won = False

    def guess(self, x, y):
        """Reveal a square on the grid and do appropriate actions based on the
        type of the square."""

        # Guessing a mine square triggers a loss.
        if self.grid_.get_square(x, y).is_bomb():
            self.lost = True
        elif self.grid_.get_square(x, y).is_number():
            self.grid_.reveal_sq(x, y)
        else:
            self.grid_.floodfill(x, y)

        # "All non-mine squares revealed" is the win condition:
        if self.grid_.revealed_count == self.grid_.nonmines:
            self.won = True

    def game_over(self):
        self.grid_.reveal_all()

    def get_status(self):
        return self.lost, self.won

    def start_timer(self):
        self.date = time.localtime()
        self.start_time = time.time()

    def stop_timer(self):
        self.end_time = time.time()

    def get_date(self):
        return self.date

    def get_time(self):
        return self.end_time - self.start_time

    def get_score(self):
        return ((1 / self.get_time()) * self.grid_.get_size()) * self.grid_.mines

    def print_grid(self):
        print(self.grid_)
