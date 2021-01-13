'''
For testing with the text version
'''

b = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            print(board[i][j], end="")
            if j == 8:
                print()
            else:
                print(" ", end="")


def find_empty_cell(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return False


def is_valid(board, target, pos):
    # Check row and col
    for i in range(len(board[0])):
        if (pos[1] != i and target == board[pos[0]][i]) or \
            (pos[0] != i and target == board[i][pos[1]]):
            return False

    # Check sub-grid
    brow = pos[0]//3
    bcol = pos[1]//3
    for i in range(3):
        for j in range(3):
            if (i, j) != pos and target == board[brow*3+i][bcol*3+j]:
                return False
    return True


def solve(board):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty
    for i in range(0, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False