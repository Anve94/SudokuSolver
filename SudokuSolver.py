from copy import deepcopy
from settings import ENABLE_DEBUG


class SudokuSolver(object):
    """ SudokuSolver class. This class requires a list representation
        of a sudoku, and will then try to solve it.

        Usage:
            Instantiate an object from the class and pass a start_board.
            Then you can use the exposed methods.
        Exposed methods:
            solve          -- Attempts to solve the sudoku
            board_is_valid -- Check wheter the board with which the
                              object is instantiated is a valid board. """

    def __init__(self, start_board):
        ''' Initializer for the SodukoSolver object.
            Requires a sudoku board as argument.
            Assumes the given board is validated.'''
        self.is_solved = False
        self.board = deepcopy(start_board)

    def solve(self, board):
        ''' Main sudoku solver routine. Note: this method works
            recursively. It's a brute-force approach (very) loosely based on
            https://en.wikipedia.org/wiki/Sudoku_solving_algorithms '''

        # Pointer to keep track of the next position to be
        # checked. Represented as next_pos[row, col].
        next_pos = [0, 0]

        # If there is no empty new location available, all
        # squares are filled in and the sudoku is considered complete.
        if not self.next_empty_location(board, next_pos):
            self.board = board
            self.is_solved = True
            return True

        # Update the current row and col to check based on the pointer.
        # Remember: the pointers were updated to represent a new square.
        current_row = next_pos[0]
        current_col = next_pos[1]

        # Go over digits 1 up to and including 9.
        # Note: start value is inclusive, end value is exclusive
        for value in range(1, 10):
            if self.is_legal_move(board, current_row,
                                  current_col, value):
                # Check if the considered move is legal
                # If it is legal, assign value to the square
                board[current_row][current_col] = value

                # Do all of the above recursively until we found a
                # solution or considered every possible value. Remember:
                # the next_pos gets updated each time. Which makes this
                # brute-force algorithm.
                if self.solve(board):
                    return True

                # If we tried all options (1 to 9) recursively and encountered
                # an error, reset the tried square to zero and try again.
                board[current_row][current_col] = 0

        # By returning false we "drop down a level" in the recursive trace.
        # This way, we can backtrack through the trace without having to keep
        # track of a regular stack/queue
        return False

    def board_is_valid(self):
        ''' Check if a given board solely exists of legal positions.
            A position is considered legal if and only if:
                - The positions value is unique in its row AND
                - The positions value is unique in its column AND
                - The positions value is unique in its 3x3 box
            A board is considered valid if all of it's inputted
            values comply with the above three rules. '''
        if ENABLE_DEBUG:
            print("GLOBAL DEBUG -- Checking to see if starting board is"
                  " valid.")
        board = self.board
        is_valid = True  # Innocent until proven otherwise
        for i, row in enumerate(board):
            for j, col in enumerate(row):
                # Temporarily unset given position, because the checked value
                # will always be set in its own row, column and box.
                _, board[i][j] = self.board[i][j], None
                # Squares containing a value of zero are unsolved and can thus
                # be skipped. Since all unsolved squares are represented by 0,
                # they will never be unique in the row, column and box.
                if _ != 0:
                    is_valid = self.is_legal_move(board, i, j, _)
                    board[i][j] = _
                    if not is_valid:
                        return is_valid
                board[i][j] = _
        return is_valid

    def exists_in_column(self, board, col, val):
        ''' Determine if a given value exists in the
            given column. '''
        for i in range(9):
            if board[i][col] == val:
                return True
        return False

    def exists_in_row(self, board, row, val):
        ''' Determine if a given value exists in the
            given row. '''
        for i in range(9):
            if board[row][i] == val:
                return True
        return False

    def exists_in_box(self, board, row, col, val):
        ''' Determine if a given value exists in the
            given 3x3 box. '''
        for i in range(3):
            for j in range(3):
                # Given row/col is not always top left of box
                # so this needs to be taken into account
                if board[i+(row - row % 3)][j+(col - col % 3)] == val:
                    return True
        return False

    def is_legal_move(self, board, row, col, val):
        ''' Takes a given row, column and value and decides wheter
            placing the value at this row/column is permitted or not.
            A move is considered legal if:
                - The value is unique to its own row
                - The value is unique to its own column
                - The value is unique to its own 3x3 box
                - The value is a value in the inclusive set of [1,9]'''
        if (not self.exists_in_column(board, col, val) and not
                self.exists_in_row(board, row, val) and not
                self.exists_in_box(board, row, col, val) and
                1 <= val <= 9):
            return True
        return False

    def next_empty_location(self, board, next_pos):
        ''' Determines the next empty location that is available
            on the board. Next_pos is a list passed in, and contains
            pointers (represented as [row, col]) to the next available
            position. If a proper new location is found, the next_pos
            pointer gets updated and True is returned. If there is no
            empty position, False is returned. '''
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    # A value of 0 is regarded as an empty square
                    # If we encounter it, we found the next empty
                    # square. Which means we can update the next_pos
                    # pointer.
                    next_pos[0] = row
                    next_pos[1] = col
                    return True
        return False

    def print_sudoku(self):
        ''' Prints a given sudoku grid to console. '''
        hor_line = "++---+---+---++---+---+---++---+---+---++"
        print(hor_line.replace('-', '='))
        for i, row in enumerate(self.board):
            cur_line = ""
            for j, val in enumerate(row):
                cur_line += "|"
                if j % 3 == 0:
                    cur_line += "|"
                if val is 0:
                    cur_line += ' . '
                else:
                    cur_line += ' {} '.format(val)
            cur_line += "||"
            print(cur_line)
            if (i+1) % 3 == 0:
                print(hor_line)


class SudokuGrid(object):
    def __init__(self, puzzle_list):
        ''' Initializer for a new SudokuGrid object.
            This class can create an empty sudoku grid,
            print a sudoku grid to console and has a method
            to manually fill a sudoku grid with values for testing
            purposes. '''
        # Create empty board
        self.board = self.create_board()
        self.board = self.fill_puzzle_start(self.board, puzzle_list)

    def create_board(self):
        ''' Creates an empty sudoku grid. '''
        num_rows = 9
        num_cols = 9
        empty_grid = [
                        [0 for cols in range(num_cols)]
                        for rows in range(num_rows)
                     ]
        return empty_grid

    def fill_puzzle_start(self, empty_grid, puzzle_list):
        ''' Allows developers to fill the sudoku grid with manual
            values for testing purposes. '''
        # Fill the grid with manual values for testing purposes
        puzzle_start = copy(empty_grid)
        # First row
        # puzzle_start = [
        #                 [5, 3, 0, 0, 7, 0, 0, 0, 0],
        #                 [6, 0, 0, 1, 9, 5, 0, 0, 0],
        #                 [0, 9, 8, 0, 0, 0, 0, 6, 0],
        #                 [8, 0, 0, 0, 6, 0, 0, 0, 3],
        #                 [4, 0, 0, 8, 0, 3, 0, 0, 1],
        #                 [7, 0, 0, 0, 2, 0, 0, 0, 6],
        #                 [0, 6, 0, 0, 0, 0, 2, 8, 0],
        #                 [0, 0, 0, 4, 1, 9, 0, 0, 5],
        #                 [0, 0, 0, 0, 8, 0, 0, 7, 9]
        #                ]

        puzzle_start = puzzle_list

        return puzzle_start

    def print_puzzle_fancy(self, board):
        ''' Prints a given sudoku grid to console. '''
        hor_line = "++---+---+---++---+---+---++---+---+---++"
        print(hor_line.replace('-', '='))
        for i, row in enumerate(board):
            cur_line = ""
            for j, val in enumerate(row):
                cur_line += "|"
                if j % 3 == 0:
                    cur_line += "|"
                if val is 0:
                    cur_line += ' . '
                else:
                    cur_line += ' {} '.format(val)
            cur_line += "||"
            print(cur_line)
            if (i+1) % 3 == 0:
                print(hor_line)
