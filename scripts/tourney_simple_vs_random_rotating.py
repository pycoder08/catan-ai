import csv
import time
import random
from pathlib import Path
from collections import Counter

from catanatron.game import Game
from catanatron.models.player import RandomPlayer, SimplePlayer, Color

RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)

COLORS = [Color.RED, Color.BLUE, Color.WHITE, Color.ORANGE]

def get_ps(state, i: int, suffix: str) -> int:
    # state.player_state keys look like "P0_ACTUAL_VICTORY_POINTS"
    return int(state.player_state.get(f"P{i}_{suffix}", 0))

def simulate(num_games: int = 500, seed: int = 123):
    random.seed(seed)

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_csv = RUNS_DIR / f"simple_vs_random_rotating_{run_id}.csv"

    simple_wins = 0
    simple_vp_total = 0
    simple_actual_vp_total = 0

    seat_win_counts = Counter()     # how often each seat index wins
    winner_color_counts = Counter() # how often each Color wins

    start = time.time()

    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "game_idx",
            "simple_seat_index",
            "winner_color",
            "simple_won",
            "P0_VP","P0_ACTUAL_VP",
            "P1_VP","P1_ACTUAL_VP",
            "P2_VP","P2_ACTUAL_VP",
            "P3_VP","P3_ACTUAL_VP",
            "seconds_elapsed"
        ])

        for g in range(num_games):
            # Rotate which seat index gets SimplePlayer
            simple_seat = g % 4

            players = []
            for i, c in enumerate(COLORS):
                if i == simple_seat:
                    players.append(SimplePlayer(c))
                else:
                    players.append(RandomPlayer(c))

            game = Game(players)
            winner_color = game.play()
            state = game.state

            # Who won by seat?
            # Since winner is a Color, find matching index in our COLORS list
            winner_seat = COLORS.index(winner_color)
            seat_win_counts[winner_seat] += 1
            winner_color_counts[str(winner_color)] += 1

            # Simple won?
            simple_won = (winner_seat == simple_seat)
            if simple_won:
                simple_wins += 1

            # VP stats
            p_vps = []
            for i in range(4):
                vp = get_ps(state, i, "VICTORY_POINTS")
                avp = get_ps(state, i, "ACTUAL_VICTORY_POINTS")
                p_vps.extend([vp, avp])

            simple_vp_total += p_vps[simple_seat*2]
            simple_actual_vp_total += p_vps[simple_seat*2 + 1]

            w.writerow([
                g,
                simple_seat,
                str(winner_color),
                int(simple_won),
                *p_vps,
                round(time.time() - start, 3),
            ])

            if (g + 1) % 50 == 0:
                print(f"{g+1}/{num_games} | Simple winrate so far: {simple_wins/(g+1):.3f}")

    print("\n=== Results ===")
    print(f"SimplePlayer winrate: {simple_wins}/{num_games} = {simple_wins/num_games:.3f}")
    print(f"SimplePlayer avg VP: {simple_vp_total/num_games:.3f}")
    print(f"SimplePlayer avg ACTUAL_VP: {simple_actual_vp_total/num_games:.3f}")

    print("\nSeat win counts (P0/P1/P2/P3):")
    total = sum(seat_win_counts.values())
    for seat in range(4):
        print(f"P{seat}: {seat_win_counts[seat]}/{total} = {seat_win_counts[seat]/total:.3f}")

    print("\nWinner colors:")
    total = sum(winner_color_counts.values())
    for k, v in winner_color_counts.most_common():
        print(f"{k:>12}: {v}/{total} = {v/total:.3f}")

    print(f"\nSaved: {out_csv}")

if __name__ == "__main__":
    simulate(num_games=500, seed=123)
