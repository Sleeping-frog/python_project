import csv
from src.utils import create_empty_board, print_boards, create_empty_board, coords_adjacent, BOARD_SIZE

def init_game_state():
    headers = ["Turn", "Player Move", "Player Result", "Bot Move", "Bot Result"]
    with open("data/game_state.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

def update_game_state(turn, player_move, player_result, bot_move, bot_result):
    with open("data/game_state.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([turn, player_move, player_result, bot_move, bot_result])

def hit(x, y, board, visible_board, ships):
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        if visible_board[x][y] == "~":
            if board[x][y] == "~":
                visible_board[x][y] = "X"
            elif board[x][y] == "S":
                visible_board[x][y] = "O"
                ship_idx = 0
                for idx, ship in enumerate(ships):
                    if (x, y) in ship:
                        ship_idx = idx
                        break
                destroyed = all(visible_board[nx][ny] == "O" for nx, ny in ships[ship_idx])
                if destroyed:
                    for x_1, y_1 in ships[ship_idx]:
                        for x_2, y_2 in coords_adjacent((x_1, y_1)):
                            if visible_board[x_2][y_2] == "~":
                                visible_board[x_2][y_2] = "X"
                    del ships[ship_idx]
            return
    raise ValueError("Invalid coordinates.")

def game_loop(player_board, player_ships, bot_board, bot_ships):
    visible_bot_board = create_empty_board()
    while True:
        if not player_ships:
            print("You have lost!")
            break
        if not bot_ships:
            print("You have won!")
            break
        
        print_boards(player_board, visible_bot_board)
        
        try:
            x_hit, y_hit = map(int, input("Enter coordinates to hit (format: x1 y1): ").split(" "))
            hit(x_hit, y_hit, bot_board, visible_bot_board, bot_ships)
        except:
            print("Invalid input!")
            continue

        