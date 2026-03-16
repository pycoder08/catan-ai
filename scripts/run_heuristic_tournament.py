import csv
import time
import random
from pathlib import Path
from collections import Counter

from catanatron.game import Game
from catanatron.models.player import RandomPlayer, Color

# Import our custom player
from heuristic_player import HeuristicPlayer

RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)

def simulate_rotating(num_games: int = 100, seed: int = 42):
    random.seed(seed)

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_csv = RUNS_DIR / f"heuristic_tourney_{run_id}.csv"

    wins = Counter()
    heuristic_win_count = 0
    start = time.time()

    COLORS = [Color.RED, Color.BLUE, Color.WHITE, Color.ORANGE]

    print(f"Starting {num_games} rotating games (HeuristicPlayer vs 3 RandomPlayers).")
    
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["game_idx", "heuristic_color", "winner", "is_heuristic_win", "seconds_elapsed"])

        for i in range(num_games):
            heuristic_idx = i % 4
            heuristic_color = COLORS[heuristic_idx]
            
            # Setup players, with HeuristicPlayer at the rotating seat
            players = []
            for j in range(4):
                if j == heuristic_idx:
                    players.append(HeuristicPlayer(COLORS[j]))
                else:
                    players.append(RandomPlayer(COLORS[j]))
                    
            try:
                game = Game(players)
                winner = game.play()
            except Exception as e:
                print(f"Error in game {i}: {e}")
                continue

            wins[str(winner)] += 1
            is_heuristic_win = (winner == heuristic_color)
            if is_heuristic_win:
                heuristic_win_count += 1
            
            w.writerow([
                i, 
                str(heuristic_color),
                str(winner), 
                is_heuristic_win,
                round(time.time() - start, 3)
            ])

            # Progress output
            if (i + 1) % 10 == 0:
                total = i + 1
                print(f"{total}/{num_games} | Heuristic winrate so far: {heuristic_win_count/total:.3f}")

    # Summary report
    print("\n--- FINAL RESULTS ---")
    print("Win rates by color:")
    for k, v in wins.most_common():
        print(f"{k:>10}: {v}/{num_games} = {v/num_games:.3f}")
        
    print(f"\nOverall HeuristicPlayer winrate: {heuristic_win_count}/{num_games} = {heuristic_win_count/num_games:.3f}")
    if heuristic_win_count / num_games > 0.25:
        print("-> Better than random! (baseline 25%)")
    else:
        print("-> Need to improve heuristics.")

    print(f"\nSaved detailed logs to: {out_csv}")

if __name__ == "__main__":
    simulate_rotating(num_games=100)
