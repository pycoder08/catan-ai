import csv
import time
import random
from pathlib import Path
from collections import Counter

from catanatron.game import Game
from catanatron.models.player import RandomPlayer, SimplePlayer, Color


RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)

def simulate(num_games: int = 500, seed: int = 123):
    random.seed(seed)

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_csv = RUNS_DIR / f"simple_vs_random_{run_id}.csv"

    wins = Counter()
    start = time.time()

    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["game_idx", "winner", "seconds_elapsed"])

        for i in range(num_games):
            players = [
                SimplePlayer(Color.RED),          # the “smarter” one
                RandomPlayer(Color.BLUE),
                RandomPlayer(Color.WHITE),
                RandomPlayer(Color.ORANGE),
            ]
            game = Game(players)
            winner = game.play()

            wins[str(winner)] += 1
            w.writerow([i, str(winner), round(time.time() - start, 3)])

            if (i + 1) % 50 == 0:
                total = i + 1
                red_wins = wins.get(str(Color.RED), 0)
                print(f"{total}/{num_games} | RED(Simple) winrate so far: {red_wins/total:.3f}")

    total = sum(wins.values())
    print("\nFinal win rates:")
    for k, v in wins.most_common():
        print(f"{k:>10}: {v}/{total} = {v/total:.3f}")

    print(f"\nSaved: {out_csv}")

if __name__ == "__main__":
    simulate(num_games=500, seed=123)
