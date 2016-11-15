import abc
import square


class Square(object, metaclass=abc.ABCMeta):
    """Abstract base class to represent squares. This class should never be
    instantiated.

    Abstract method:
        __str__: Returns appropriate printable human friendly string
                 representation of the square.

    Methods:
        get_pos: Returns square's position as coordinate tuple (pos_x, pos_y).
        reveal: Mark square as revealed. Sets self.revealed to True.

        is_x methods return true if square is instance of class x.
        is_bomb: See above.
        is_empty: See above.
        is_number: See above.
    """

    @abc.abstractmethod
    def __str__(self): pass

    def get_pos(self):
        return self.pos_x, self.pos_y

    def reveal(self):
        self.revealed = True

    def is_bomb(self):
        if isinstance(self, square.Bomb):
            return True
        else:
            return False

    def is_empty(self):
        if isinstance(self, square.Empty):
            return True
        else:
            return False

    def is_number(self):
        if isinstance(self, square.Number):
            return True
        else:
            return False


class Empty(Square):
    """Empty square. Has no adjacent bombs."""

    def __init__(self, pos_x, pos_y):
        super(Empty, self).__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.revealed = False

    def __str__(self):
        if self.revealed:
            return "| |"
        else:
            return "|-|"


class Bomb(Square):
    """Bomb square."""

    def __init__(self, pos_x, pos_y):
        super(Bomb, self).__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.revealed = False

    def __str__(self):
        if self.revealed:
            return "|*|"
        else:
            return "|-|"


class Number(Square):
    """Number square. Has one to eigth adjacent bomb squares."""

    def __init__(self, pos_x, pos_y, count):
        super(Number, self).__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.count = count
        self.revealed = False

    def __str__(self):
        if self.revealed:
            return "|{}|".format(self.count)
        else:
            return "|-|"
