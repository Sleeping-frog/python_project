from src.ship_input import get_player_board, save_ships_to_csv
from src.bot_generation import generate_bot_board, save_ships_to_csv as save_bot_csv
from src.gameplay import init_game_state, game_loop

def main():
    # 1. Get player ships
    #player_board, player_ships = get_player_board()
    player_board, player_ships = generate_bot_board()
    save_ships_to_csv(player_ships)
    
    # 2. Generate bot ships
    bot_board, bot_ships = generate_bot_board()
    save_bot_csv(bot_ships)
    
    # 3. Initialize game state
    init_game_state()

    game_loop(player_board, player_ships, bot_board, bot_ships)
    

if __name__ == "__main__":
    main()