
from catanatron.game import Game
from catanatron.models.player import Player, Color, RandomPlayer
import inspect

class ProbePlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def decide(self, game, playable_actions):
        print(f"ProbePlayer.decide called!")
        print(f"Type of game: {type(game)}")
        print(f"Type of playable_actions: {type(playable_actions)}")
        if len(playable_actions) > 0:
            print(f"Sample action: {playable_actions[0]}")
            print(f"Action attributes: {dir(playable_actions[0])}")
        
        # return random action to continue
        import random
        return random.choice(playable_actions)

def probe():
    print("Probing Player class...")
    print(dir(Player))
    
    print("\nStarting probe game...")
    players = [
        ProbePlayer(Color.RED),
        RandomPlayer(Color.BLUE),
        RandomPlayer(Color.WHITE),
        RandomPlayer(Color.ORANGE),
    ]
    game = Game(players)
    # Play one turn or until probe is called
    try:
        game.play()
    except Exception as e:
        print(f"Game ended or crashed: {e}")

if __name__ == "__main__":
    probe()
