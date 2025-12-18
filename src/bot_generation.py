import csv
import random
from src.utils import create_empty_board, is_valid_ship_position, coords_adjacent

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def generate_bot_board():
    board = create_empty_board()
    ships = []

    for size in SHIP_SIZES:
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            horizontal = random.choice([True, False])
            coords = [(x+i, y) if horizontal else (x, y+i) for i in range(size)]
            if is_valid_ship_position(board, coords):
                for cx, cy in coords:
                    board[cx][cy] = "S"
                ships.append(coords)
                break
    return (board, ships)

def save_ships_to_csv(ships, filename="data/bot_ships.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for ship in ships:
            writer.writerow([f"{x}-{y}" for x, y in ship])

if __name__ == "__main__":
    ships = generate_bot_board()
    save_ships_to_csv(ships)