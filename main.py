'''
Sudoku Solver (version 1.0)
Allows a player to place numbers on a sudoku board and solve the board at anytime
-------------------------------------
Commands:
  To quit: close the window or press "Esc"
  To reset the board: press "R"
  To guess a number: choose a position and press any number key from 1-9
  To commit to a number: choose a position with a guessed number and press "Enter"
  To delete a guessed number or a committed number: press "Delete" or "Backspace"
  To solve the current sudoku board: press the Spacebar
-------------------------------------
Notes:
  The player can quit anytime, even during the solving process
  The player won't be able to commit to an invalid number
  In the solve_gui function in the Grid class, the delay time could be changed
  Some boards can take quite long we are showing everytime step in the solving process
'''

import sys
import pygame
from solver import is_valid, find_empty_cell


class Grid:
    '''
    An object that respresent the sudoku board.
    Fields:
        size (Int),
        screen (Surface),
        selected (anyof None (tuple Int Int)),
        squares (listof (listof Square)),
        board (listof (listof Int))
    '''

    def __init__(self, size, screen):
        '''
        Initialize self as a Grid object with the given size and the object screen. Returns None.

        Effects: Mutates self

        __init__: Int Suface -> None
        '''
        self.size = size
        self.screen = screen
        self.selected = None
        self.squares = []
        for i in range(9):
            L = []
            for j in range(9):
                L.append(Square(0, i, j, size//9, False, False))
            self.squares.append(L)
        self.board = []
        self.update_board()

    def update_board(self):
        '''
        Returns None.
        Makes the (listof (listof Int)) board a numerical representation of the sudoku board.

        Effects: Mutates self.board

        update_board: Grid -> None
        '''
        self.board = []
        for i in range(9):
            L = []
            for j in range(9):
                L.append(self.squares[i][j].num)
            self.board.append(L)

    def clear_square(self, normal):
        '''
        Returns None.
        Clears the selected square on normal mode, clears all squares otherwise.

        Effects: Mutates Square oject in self.squares

        clear_square: Grid Bool -> None
        '''
        if normal:
            row, col = self.selected
            self.squares[row][col].set(0)
            self.squares[row][col].set_temp(0)
            self.squares[row][col].set_fixed(False)
        else:
            for row in self.squares:
                for square in row:
                    square.set(0)
                    square.set_temp(0)
                    square.set_fixed(False)

    def put_temp(self, val):
        '''
        Change the temp value in the selected square and returns None.

        Effects: Mutates temp in the selected Square object.

        put_temp: Grid Int -> None
        '''
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    def put_num(self, val):
        '''
        Returns None if the selected square already has a num value > 0.
        If the number is valid, places it in the selected square and returns True.
        Return False otherwise.

        Effects: Mutates the select square and self.squares

        put_num: Grid Int -> anyof Bool None
        '''
        row, col = self.selected
        if self.squares[row][col].num == 0:
            if is_valid(self.board, val, (row, col)):
                self.squares[row][col].set(val)
                self.squares[row][col].set_fixed(True)
                self.update_board()
                return True
            return False

    def draw_board(self):
        '''
        Draws the grid and squares in the game window and returns None.

        Effects: Draws the grid and squares in the game window.

        draw: Grid -> None
        '''
        # Draw grid
        gap = self.size//9
        for i in range(10):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i*gap),
                             (self.size, i*gap), thick)
            pygame.draw.line(self.screen, (0, 0, 0), (i * gap, 0),
                             (i * gap, self.size), thick)

        # Draw squares
        for i in range(9):
            for j in range(9):
                self.squares[i][j].draw_square(self.screen)

    def click(self, coor):
        '''
        Returns the simplied coordination tuple relative to the game board, return None if the click
        is out of the game board.

        click: Grid (tuple Int Int) -> anyof (tuple Int Int) None
        '''
        if coor[0] < self.size and coor[1] < self.size:
            gap = self.size // 9
            x = coor[0] // gap
            y = coor[1] // gap
            return (y, x)

    def select(self, row, col):
        '''
        Selects the square according to row and col, returns None.

        Effects:
            Mutates the selected field of the selected square.
            Mutates self.selected

        select: Grid Int Int -> None
        '''
        # Unselect the currently selected square if applicable
        if self.selected:
            r = self.selected[0]
            c = self.selected[1]
            self.squares[r][c].selected = False

        # Select the desired square
        self.squares[row][col].selected = True
        self.selected = (row, col)

    def solve_gui(self):
        '''
        Solves the sudoku board using the back tracking algorithm.
        Draws out every guess made in the process.

        Effects:
            Draws to the window.
            Mutates self.board.
            Mutates Square objects.

        solve_gui: Grid -> anyof None Bool
        '''
        self.update_board()
        cell = find_empty_cell(self.board)
        if not cell:
            return True
        row, col = cell

        for i in range(1, 10):
            if is_valid(self.board, i, (row, col)):

                # Handling events so system doesn't think the game is crashing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sys.exit()

                self.board[row][col] = i
                self.squares[row][col].set(i)
                self.squares[row][col].draw_square_change(self.screen, True)
                self.update_board()
                pygame.display.update()
                # Add delay to show each step better
                pygame.time.delay(3)

                if self.solve_gui():
                    return True

                self.board[row][col] = 0
                self.squares[row][col].set(0)
                self.update_board()
                self.squares[row][col].draw_square_change(self.screen, False)
                pygame.display.update()

        return False

    def change_state(self, boo):
        '''
        Change the solving state of all Square objects in self.squares to boo and returns None.

        Effects: Mutates all Square objects in self.squares.

        change_state: Grid Bool -> None
        '''
        for listtemp in self.squares:
            for square in listtemp:
                square.set_solving(boo)


class Square:
    '''
    An object that respresent each square in the sudoku board.
    Fields:
        num (Int),
        temp (Int),
        row (Int),
        col (Int),
        size (Int),
        solving (Bool),
        fixed (Bool),
        selected (Bool)
    '''

    def __init__(self, num, row, col, size, solving, fixed):
        self.num = num
        self.temp = 0
        self.row = row
        self.col = col
        self.size = size
        self.solving = solving
        self.fixed = fixed
        self.selected = False

    def set(self, val):
        '''
        Sets the num value to val.

        Effects: Mutates self.num.

        set: Square Int -> None
        '''
        self.num = val

    def set_temp(self, val):
        '''
        Sets the temp value to val.

        Effects: Mutates self.temp.

        set: Square Int -> None
        '''
        self.temp = val

    def set_fixed(self, boo):
        '''
        Sets the fixed value to boo.

        Effects: Mutates self.fixed.

        set: Square Bool -> None
        '''
        self.fixed = boo

    def set_solving(self, boo):
        '''
        Sets the solving value to boo.

        Effects: Mutates self.solving.

        set: Square Bool -> None
        '''
        self.solving = boo

    def draw_square(self, screen):
        '''
        Draws the square to the screen when not on solving mode.

        Effects: Draws the square to the screen.

        draw: Square Surface -> None
        '''
        font = pygame.font.Font("freesansbold.ttf", 30)
        color = (0, 0, 0)
        if self.solving and not self.fixed:
            color = (189, 121, 19)
        gap = self.size
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.num == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            screen.blit(text, (x+5, y+5))
        elif not self.num == 0:
            text = font.render(str(self.num), True, color)
            screen.blit(text, (x + (gap/2 - text.get_width()/2),
                               y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_square_change(self, screen, changed):
        '''
        Draws the square to the screen when on solving mode.

        Effects: Draws the square to the screen.

        draw: Square Surface Bool -> None
        '''
        font = pygame.font.Font("freesansbold.ttf", 30)
        color = (0, 0, 0)
        if self.solving and not self.fixed:
            color = (189, 121, 19)
        gap = self.size
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(screen, (255, 255, 237), (x, y, gap, gap), 0)

        text = font.render(str(self.num), True, color)
        screen.blit(text, (x + (gap / 2 - text.get_width() / 2),
                           y + (gap / 2 - text.get_height() / 2)))
        if changed:
            pygame.draw.rect(screen, (255, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(screen, (0, 0, 255), (x, y, gap, gap), 3)


def show_instructions():
    '''
    Blit the instructions at the bottom of the game window.

    show_instructions: None -> None
    '''
    ins1 = INS_FONT.render(INS_TEXT1, True, (0, 0, 0))
    ins2 = INS_FONT.render(INS_TEXT2, True, (0, 0, 0))
    screen.blit(ins1, (10, HEIGHT-45))
    screen.blit(ins2, (10, HEIGHT-25))


def restart():
    '''
    Reset the board.

    restart: None -> None
    '''
    sudoku.clear_square(False)
    sudoku.change_state(False)
    sudoku.update_board()


if __name__ == "__main__":
    # Initialize the pygame
    pygame.init()

    # Initialize constants
    HEIGHT = 600
    WIDTH = 540
    BG_COLOR = (230, 230, 250)
    INS_FONT = pygame.font.Font("freesansbold.ttf", 17)
    INS_TEXT1 = "Press Enter to place number"
    INS_TEXT2 = "Press Space to solve"

    # Screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BG_COLOR)

    # Title and icon
    pygame.display.set_caption("Sudoku Solver")
    icon = pygame.image.load("sudoku.png")
    pygame.display.set_icon(icon)

    # Running part
    sudoku = Grid(540, screen)
    k = None

    # Game loop
    while True:
        # Handling events
        for event in pygame.event.get():
            # Quit by close the window
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Quit by the Escape key
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    restart()
                if event.key == pygame.K_1:
                    k = 1
                if event.key == pygame.K_2:
                    k = 2
                if event.key == pygame.K_3:
                    k = 3
                if event.key == pygame.K_4:
                    k = 4
                if event.key == pygame.K_5:
                    k = 5
                if event.key == pygame.K_6:
                    k = 6
                if event.key == pygame.K_7:
                    k = 7
                if event.key == pygame.K_8:
                    k = 8
                if event.key == pygame.K_9:
                    k = 9
                # Delete a number from a square
                if (event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE) and sudoku.selected:
                    sudoku.clear_square(True)
                    k = None
                # Start solving
                if event.key == pygame.K_SPACE:
                    sudoku.change_state(True)
                    sudoku.solve_gui()
                # Enter a number, also checks if that number is valid
                if event.key == pygame.K_RETURN and sudoku.selected:
                    i, j = sudoku.selected
                    if sudoku.squares[i][j].temp != 0:
                        sudoku.put_num(sudoku.squares[i][j].temp)
                        k = None

            # Click to choose the square
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = sudoku.click(pos)
                if clicked:
                    sudoku.select(clicked[0], clicked[1])
                    k = None

        # Pencil the number
        if sudoku.selected and k is not None:
            sudoku.put_temp(k)

        # Update screen
        screen.fill(BG_COLOR)
        sudoku.draw_board()
        show_instructions()
        pygame.display.update()
