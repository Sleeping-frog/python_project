import random
from src.utils import BOARD_SIZE, coords_adjacent

class BattleshipBot:
    def __init__(self):
        self.mode = "random"   # random, follow, axis
        self.last_hits = []    # coordinaes of current ship
        self.axis = None       # "horizontal" or "vertical"
        self.possible_targets = set((x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE))

    def choose_move(self):
        if self.mode == "random":
            move = random.choice(list(self.possible_targets))
        elif self.mode == "follow":
            move = self.get_follow_move()
        elif self.mode == "axis":
            move = self.get_axis_move()

        self.possible_targets.remove(move)
        return move

    def get_follow_move(self):
        x, y = self.last_hits[0]
        neighbors = [(x+i, y+j) for i, j in [(-1,0),(1,0),(0,-1),(0,1)]]
        neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) in self.possible_targets]
        if neighbors:
            return random.choice(neighbors)
        else:
            self.mode = "random"
            self.last_hits.clear()
            return self.choose_move()

    def get_axis_move(self):
        x1, y1 = self.last_hits[0]
        x2, y2 = self.last_hits[1]

        if x1 == x2:
            self.axis = "horizontal"
        else:
            self.axis = "vertical"

        targets = []
        if self.axis == "horizontal":
            row = x1
            for col_offset in [-1,1]:
                col = self.last_hits[-1][1] + col_offset
                if 0 <= col < BOARD_SIZE and (row, col) in self.possible_targets:
                    targets.append((row, col))
        else:  # vertical
            col = y1
            for row_offset in [-1,1]:
                row = self.last_hits[-1][0] + row_offset
                if 0 <= row < BOARD_SIZE and (row, col) in self.possible_targets:
                    targets.append((row, col))

        if targets:
            return random.choice(targets)
        else:
            self.mode = "random"
            self.last_hits.clear()
            self.axis = None
            return self.choose_move()

    def process_result(self, move, result, ship_coords):
        if result == "hit":
            self.last_hits.append(move)
            if len(self.last_hits) == 1:
                self.mode = "follow"
            elif len(self.last_hits) >= 2:
                self.mode = "axis"
        elif result == "sink":
            self.last_hits.clear()
            self.axis = None
            self.mode = "random"
            for x_1, y_1 in ship_coords:
                for x_2, y_2 in coords_adjacent((x_1, y_1)):
                    self.possible_targets.discard((x_2, y_2))