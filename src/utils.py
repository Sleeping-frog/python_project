import random

BOARD_SIZE = 10

def create_empty_board():
    return [["~" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def clear_terminal():
    print("\033[2J\033[H", end="")

def print_board(board):
    clear_terminal()
    cell_width = 3
    for num in [" "] + list(range(BOARD_SIZE)):
        print(f"{num:^{cell_width}}", end="")
    print()
    for idx, row in enumerate(board):
        for cell in [idx] + row:
            print(f"{cell:^{cell_width}}", end="")  # centering output
        print()

def print_boards(board_player, board_bot):
    clear_terminal()
    cell_width = 3
    for num in [" "] + list(range(BOARD_SIZE)) + [" ", " "] + list(range(BOARD_SIZE)):
        print(f"{num:^{cell_width}}", end="")
    print()
    for idx in range(len(board_player)):
        for cell in [idx] + board_player[idx]:
            print(f"{cell:^{cell_width}}", end="")
        print(f"{" ":^{cell_width}}", end="")
        for cell in [idx] + board_bot[idx]:
            print(f"{cell:^{cell_width}}", end="")
        print()

def coords_adjacent(coord):
    x, y = coord
    return [
        (x+i, y+j)
        for i in [-1, 0, 1]
        for j in [-1, 0, 1]
        if 0 <= x+i < BOARD_SIZE and 0 <= y+j < BOARD_SIZE and (i != 0 or j != 0)
    ]

def is_valid_ship_position(board, ship_coords):
    for x, y in ship_coords:
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return False
        if board[x][y] != "~":
            return False
        for nx, ny in coords_adjacent((x, y)):
            if board[nx][ny] != "~":
                return False
    return True