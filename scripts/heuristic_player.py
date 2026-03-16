from catanatron.models.player import Player
import random

class HeuristicPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def decide(self, game, playable_actions):
        if not playable_actions:
            return None
            
        best_actions = []
        best_score = -float('inf')
        
        for action in playable_actions:
            score = self.score_action(game, action)
            if score > best_score:
                best_score = score
                best_actions = [action]
            elif score == best_score:
                best_actions.append(action)
                
        # Break ties randomly among the best actions
        return random.choice(best_actions)

    def score_action(self, game, action):
        """
        Assigns a score to an action. Higher is better.
        """
        if isinstance(action, tuple) and len(action) > 0:
            action_type = action[0]
        elif hasattr(action, 'action_type'):
            action_type = action.action_type
        else:
            return 0

        action_name = str(action_type).split('.')[-1]
        
        # Base scores defining the heuristic's priorities
        scores = {
            "BUILD_CITY": 100,
            "BUILD_SETTLEMENT": 80,
            "PLAY_MONOPOLY": 40,
            "PLAY_YEAR_OF_PLENTY": 35,
            "PLAY_ROAD_BUILDING": 30,
            "BUY_DEV_CARD": 25,
            "PLAY_KNIGHT": 20,
            "BUILD_ROAD": 10,
            "MOVE_ROBBER": 15,
            "MARITIME_TRADE": 5,
            "ROLL": 500, # Always roll if available (highest priority)
            "DISCARD": 0, 
            "END_TURN": -10, # Heavily penalize ending turn if we can do something else
        }

        score = scores.get(action_name, 0)
        
        # Action-specific context tweaks
        if action_name == 'MARITIME_TRADE':
            # Trading is usually only good if we have an excess of one resource
            # and need another. In Catanatron, actions might contain (give_res, take_res)
            # giving it a slightly lower score ensures we build/buy first if possible.
            score = 5 
            
        elif action_name == 'DISCARD':
            # We want to randomly discard, but prefer to keep valuable resources. 
            # In a basic heuristic, all discards are equivalent unless we inspect resources.
            score = random.randint(0, 5) 

        elif action_name == 'PLAY_KNIGHT':
            # Playing a knight before rolling is often good, or if robber is on us.
            score += random.randint(0, 10)

        elif action_name == 'MOVE_ROBBER':
            # Try to place it anywhere
            score += random.randint(0, 5)

        # Tie-breaker: prefer anything over END_TURN if it has no base score
        if score == 0 and 'END_TURN' not in action_name:
            score = 1
            
        return score
