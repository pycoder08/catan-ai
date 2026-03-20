import uuid
import json
import pickle
import psycopg2
import random

import gymnasium as gym
try:
    import catanatron_gym
except ImportError:
    pass

from catanatron.json import GameEncoder
from catanatron.game import Game

DB_URL = "postgresql://catanatron:victorypoint@localhost:5432/catanatron_db"

def play_and_visualize():
    print("Connecting to local Docker Database...")
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    cur = conn.cursor()

    match_uuid = str(uuid.uuid4())
    print(f"Starting Match UUID: {match_uuid}")

    env = gym.make("catanatron-v1")
    obs, info = env.reset()

    # Function to emulate the Catanatron web insertion
    def log_state(game, index):
        state_json = json.dumps(game, cls=GameEncoder)
        pickled = pickle.dumps(game)
        cur.execute(
            "INSERT INTO game_states (uuid, state_index, state, pickle_data) VALUES (%s, %s, %s, %s)",
            (match_uuid, index, state_json, pickled)
        )

    print("Agent is playing...")
    done = False
    
    while not done:
        # A valid random agent
        action = random.choice(info["valid_actions"])
        
        step_result = env.step(action)
        if len(step_result) == 4:
            obs, reward, terminated, info = step_result
            truncated = False
        else:
            obs, reward, terminated, truncated, info = step_result
            
        done = terminated or truncated

    final_game = env.unwrapped.game
    winning_color = final_game.winning_color()
    print(f"Game Finished! Winner: {winning_color}")

    print("Recreating and saving EVERY single frame of the game history...")
    replay_game = Game(
        players=env.unwrapped.players,
        catan_map=final_game.state.board.map,
        seed=final_game.seed,
        vps_to_win=final_game.vps_to_win
    )
    
    # Log empty initial board state
    log_state(replay_game, 0)
    
    # Log every single step linearly!
    for i, historical_record in enumerate(final_game.state.action_records):
        replay_game.execute(historical_record.action, validate_action=False, action_record=historical_record)
        log_state(replay_game, i + 1)

    print("\nSUCCESS! All game states saved to database.")
    print(f"-> Go to http://localhost:3000/replays/{match_uuid} to watch the game replay!")

if __name__ == "__main__":
    play_and_visualize()
