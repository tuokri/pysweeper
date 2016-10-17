"""Minesweeper main module for CLI interaction with user and
file I/O for long term score storing.
"""

import os
import re
import csv
import sys
import grid
import time
import minesweeper as ms

# Maximum grid size is limited due to
# printing problems with increasing row and column numbers and
# the dimensions of the CLI window.
MAX_SIZE_X = 25
MAX_SIZE_Y = 25

# Regular expression pattern for checking validity of user input coordinates.
# Breakdown of regex:
# ^ anchor at the start of the string.
# \d+ match 1 or more characters that are digits.
# \, match a comma.
# \d+ match 1 or more characters that are digits.
# $ anchor at the end of the string.
XY_FORMAT = "^\d+\,\d+$"

DATE_FORMAT = "%c"
SELECTIONS = ["s", "p", "q"]
SEL_STRINGS = ["S to view highscores.", "P to play a new game.", "Q to quit."]
SCOREFILE = "msscores.dat"
WELCOMEFILE = "welcome.dat"


def _print_welcome():
    welcomestr = ""

    try:
        with open(WELCOMEFILE, "r") as target:
            for line in target:
                welcomestr += line
    except (IOError, FileNotFoundError):
        print("WELCOME TO MINESWEEPER!")

    print(welcomestr)


def _print_scores():
    _clear()
    print("HIGH SCORES TOP 15")
    scores = _read_scores(SCOREFILE)
    scores.sort(key=lambda scores: scores[1], reverse=True)
    try:
        for i in range(15):
            print("Player: {} - Score: {:.2f} - Date: {}.".format(
                scores[i][0], float(scores[i][1]), scores[i][2]))
    except IndexError:
        pass


def _get_player():
    """Get the player name as input from the user and check its validity."""

    print()
    while True:
        try:
            player = input("Enter player name (max 16 characters): ")
            if not player:
                raise ValueError("Player name is required.")
            if len(player) > 16:
                raise ValueError("Player name is too long.")
            return player
        except ValueError as e:
            print(e)


def _get_coordinates(lim_x, lim_y):
    """Get coordinates as input from the user and check their validity."""

    p = re.compile(XY_FORMAT)

    while True:
        try:
            coords = (input("\nEnter coordinates as x,y : "))
            if not coords:
                raise ValueError("Please enter coordinates.")
            elif not p.match(coords):
                raise ValueError("Enter two coordinates separated by a comma.")
            else:
                coords = list(map(int, coords.split(",")))
            if not _check_coordinates(coords, (lim_x - 1, lim_y - 1)):
                raise ValueError("Out of grid.")
            else:
                return coords
        except TypeError:
            print("Enter coordinates as integers.")
        except ValueError as e:
            print(e)


def _get_selection():
    print()
    for s in range(len(SELECTIONS)):
        print("{}".format(SEL_STRINGS[s]))
    while True:
        try:
            s = input("Select action and press enter: ").lower()
            if s not in SELECTIONS:
                raise ValueError("Please choose a valid option.")
            return s
        except ValueError as e:
            print(e)


def _get_mines(size_x, size_y):
    print("\nChoose amount of mines and press enter.")
    print("You may choose 1 to {} mines.".format(size_x * size_y))
    while True:
        try:
            m = int(input("Enter amount of mines: "))
            if m <= 0:
                print("Amount of mines must be greater than zero.")
                continue
            elif not m:
                print("Amount of mines is required.")
                continue
            return m
        except (TypeError, ValueError):
            print("Enter amount of mines as an integer.")


def _get_grid_size():
    """Get size for grid as input from the user and check their validity."""

    p = re.compile(XY_FORMAT)

    print("\nMaximum size for grid is {} * {}".format(MAX_SIZE_X, MAX_SIZE_Y))
    while True:
        try:
            size = (input("Enter grid size as width,height: "))
            if not size:
                raise ValueError("Dimensions are required.")
            elif not p.match(size):
                raise ValueError("Enter two dimensions separated by a comma.")
            else:
                size = list(map(int, size.split(",")))
            if size[0] <= 0 or size[1] <= 0:
                raise ValueError("Width and height must be greater than zero.")
            if not _check_coordinates(size, (MAX_SIZE_X, MAX_SIZE_Y)):
                raise ValueError("Maximum grid size exceeded.")
            else:
                return size
        except TypeError:
            print("Enter dimensions as integers.")
        except ValueError as e:
            print(e)


def _check_coordinates(coords, size):
    """Check that coordinates are inside the grid given as an argument.

    Args:
        coords: (x, y) tuple.
        size: (size_x, size_y) tuple.
    """

    x, y = coords
    size_x, size_y = size

    if x > size_x or y > size_y:
        return False
    elif x < 0 or y < 0:
        return False
    else:
        return True


def _read_scores(file):
    scores = []

    try:
        with open(file, "r", newline="") as target:
            reader = csv.reader(target)
            for line in reader:
                scores.append(line)
    except (IOError, FileNotFoundError):
        print("Cannot read scores from file.")
        return []

    return scores


def _write_scores(file, scores):
    """Scorelist should be a two-dimensional list formatted as:

    [["player", score, date]]

    Where dates are time_struct objects.
    Dates are formated before writing to file.
    """

    try:
        with open(file, "a", newline="") as target:
            writer = csv.writer(target)
            for i in range(len(scores)):
                scores[i][2] = _format_date(scores[i][2], DATE_FORMAT)
            for score in scores:
                writer.writerow(score)
    except IOError:
        print("Cannot write scores to file.")


def _clear():
    """Clears CLI screen. Works on MS-DOS and Unix."""

    os.system("cls" if os.name == "nt" else "clear")


def _format_date(date, format_):
    """Returns date (time_struct object)
    as a string formatted to specified format.
    """

    return "{}".format(time.strftime(format_, date))


def main():
    _print_welcome()
    sel = _get_selection()

    if sel == "q":
        sys.exit(1)
    elif sel == "s":
        _print_scores()
    elif sel == "p":
        player = _get_player()
        size_x, size_y = _get_grid_size()
        mines = _get_mines(size_x, size_y)
        game = ms.Minesweeper(grid.Grid(size_x, size_y, mines))
        game.start_timer()
        lost, won = game.get_status()

        while not lost and not won:
            _clear()
            game.print_grid()
            x, y = _get_coordinates(size_x, size_y)
            game.guess(x, y)
            lost, won = game.get_status()

        game.game_over()
        game.stop_timer()
        _clear()
        game.print_grid()

        gametime = game.get_time()
        gamedate = game.get_date()
        gamescore = game.get_score()

        if lost:
            print("You lost!")
        else:
            print("Congratulations {}, you won!".format(player))
            print("Your score is {:.2f} points.".format(gamescore))
            print("The game lasted {:.2f} seconds.".format(gametime))
            print("The date is {}".format(_format_date(gamedate, DATE_FORMAT)))
            print("Saving score to file.")
            _write_scores(SCOREFILE, [[player, gamescore, gamedate]])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
