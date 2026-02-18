from catanatron.game import Game
from catanatron.models.player import RandomPlayer, SimplePlayer, Color

def try_print_vp(state):
    # Common patterns across versions:
    # - state.player_state[color].victory_points
    # - state.player_states[color].victory_points
    # - state.players[color].victory_points
    for container_name in ["player_state", "player_states", "players"]:
        container = getattr(state, container_name, None)
        if container is None:
            continue
        # container might be dict-like keyed by Color
        try:
            for c in [Color.RED, Color.BLUE, Color.WHITE, Color.ORANGE]:
                ps = container[c]
                vp = getattr(ps, "victory_points", None)
                if vp is not None:
                    print(f"  {container_name}[{c}].victory_points = {vp}")
                else:
                    # Sometimes VP is a method or property with different name
                    for alt in ["vp", "points", "public_victory_points", "total_victory_points"]:
                        if hasattr(ps, alt):
                            print(f"  {container_name}[{c}].{alt} = {getattr(ps, alt)}")
                            break
            return True
        except Exception:
            # Not keyed by Color, or structure differs
            continue
    return False

def main():
    for g in range(3):
        players = [
            SimplePlayer(Color.RED),
            RandomPlayer(Color.BLUE),
            RandomPlayer(Color.WHITE),
            RandomPlayer(Color.ORANGE),
        ]
        game = Game(players)
        winner = game.play()

        print(f"\nGame {g} winner: {winner}")

        state = getattr(game, "state", None)
        if state is None:
            print("No game.state attribute found.")
            continue

        printed = try_print_vp(state)
        if not printed:
            print("Couldn't find VP fields. Dumping state attributes that look relevant:")
            for name in dir(state):
                if any(k in name.lower() for k in ["player", "victory", "point", "score", "vp"]):
                    print(" -", name)

if __name__ == "__main__":
    main()
