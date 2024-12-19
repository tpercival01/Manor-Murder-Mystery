from GameState import GameState
from GameLoop import run_game_loop

def main():
    # TODO: Add a load save function

    # Create new game state
    game_state = GameState()

    # Start the game loop with the new game state
    run_game_loop(game_state)

if __name__ == "__main__":
    main()