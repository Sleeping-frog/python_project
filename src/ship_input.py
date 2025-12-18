import csv
from src.utils import create_empty_board, print_board, is_valid_ship_position

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def get_player_board():
    board = create_empty_board()
    ships = []
    
    print_board(board)
    for size in SHIP_SIZES:
        while True:
            coords_input = input(f"Enter coordinates for a ship of size {size} (format: x1 y1 x2 y2): ")
            coords_input = list(map(int, coords_input.split(" ")))
            coords = list(zip(coords_input[::2], coords_input[1::2]))

            if size > 1:
                if coords[0][0] == coords[1][0]:                                                        # ship is vertical
                    if coords[0][1] < coords[1][1]:
                        coords = [(coords[0][0], y) for y in range(coords[0][1], coords[1][1] + 1)]
                    else:
                        coords = [(coords[0][0], y) for y in range(coords[1][1], coords[0][1] + 1)]

                elif coords[0][1] == coords[1][1]:                                                       # ship is horizontal
                    if coords[0][0] < coords[1][0]:
                        coords = [(x, coords[0][1]) for x in range(coords[0][0], coords[1][0] + 1)]
                    else:
                        coords = [(x, coords[0][1]) for x in range(coords[1][0], coords[0][0] + 1)]
                else:
                    print("Coordinates aren't in one dimension!")
                    continue
            elif coords[0] != coords[1]:
                print("For size 1 ships pairs of coordinates must be the same!")
            else:
                coords = coords[0:1]


            if len(coords) != size:
                print("Wrong ship size!")
                continue

            if is_valid_ship_position(board, coords):
                for x, y in coords:
                    board[x][y] = "S"
                ships.append(coords)
                print_board(board)
                break
            else:
                print("Invalid position or the ship is touching another one!")
    return (board, ships)

def save_ships_to_csv(ships, filename="data/player_ships.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for ship in ships:
            writer.writerow([f"{x}-{y}" for x, y in ship])

if __name__ == "__main__":
    ships = get_player_board()
    save_ships_to_csv(ships)