import random
from collections import Counter

# Catanatron docs show two import styles; this one matches the readthedocs example.
from catanatron.game import Game
from catanatron.models.player import RandomPlayer, Color


def run_games(num_games: int = 100, seed: int = 0):
    random.seed(seed)

    wins = Counter()

    for i in range(num_games):
        players = [
            RandomPlayer(Color.RED),
            RandomPlayer(Color.BLUE),
            RandomPlayer(Color.WHITE),
            RandomPlayer(Color.ORANGE),
        ]
        game = Game(players)
        winner_color = game.play()  # returns winning Color
        wins[str(winner_color)] += 1

        if (i + 1) % 10 == 0:
            print(f"Completed {i+1}/{num_games} games...")

    print("\nWin counts:")
    for k, v in wins.most_common():
        print(f"{k:>10}: {v}")

    return wins


if __name__ == "__main__":
    run_games(num_games=100, seed=42)
