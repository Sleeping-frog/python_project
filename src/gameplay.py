import csv
from src.utils import create_empty_board, print_boards, create_empty_board, coords_adjacent, BOARD_SIZE
from src.bot_AI import BattleshipBot

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
                return ("miss", None)
            elif board[x][y] == "S":
                visible_board[x][y] = "O"
                ship_idx = 0
                for idx, ship in enumerate(ships):
                    if (x, y) in ship:
                        ship_idx = idx
                        break
                destroyed = all(visible_board[nx][ny] == "O" for nx, ny in ships[ship_idx])
                if destroyed:
                    ship_coords = ships[ship_idx]
                    for x_1, y_1 in ships[ship_idx]:
                        for x_2, y_2 in coords_adjacent((x_1, y_1)):
                            if visible_board[x_2][y_2] == "~":
                                visible_board[x_2][y_2] = "X"
                    del ships[ship_idx]
                    return ("sink", ship_coords)
                return ("hit", None)
    raise ValueError("Invalid coordinates.")

def game_loop(player_board, player_ships, bot_board, bot_ships):
    visible_bot_board = create_empty_board()
    visible_player_board = create_empty_board()
    bot = BattleshipBot()
    turn = 0
    while True:
        turn += 1
        print_boards(player_board, visible_bot_board)
        
        xp_hit, yp_hit = (0, 0)
        resultp = ""
        try:
            xp_hit, yp_hit = map(int, input("Enter coordinates to hit (format: x1 y1): ").split(" "))
            resultp, tmp = hit(xp_hit, yp_hit, bot_board, visible_bot_board, bot_ships)
        except:
            print("Invalid input!")
            continue

        if not bot_ships:
            print("You have won!")
            break

        xb_hit, yb_hit = bot.choose_move()
        resultb, ship_coords = hit(xb_hit, yb_hit, player_board, visible_player_board, player_ships)
        bot.process_result((xb_hit, yb_hit), resultb, ship_coords)

        
        if not player_ships:
            print("You have lost!")
            break

        update_game_state(turn, (xp_hit, yp_hit), resultp, (xb_hit, yb_hit), resultb)
        