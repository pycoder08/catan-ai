from catanatron.models.player import Player
from catanatron.game import ActionType
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
        # Catanatron Action objects can vary slightly by version.
        # They are usually tuples where the first element is the ActionType enum.
        if isinstance(action, tuple) and len(action) > 0:
            action_type = action[0]
        elif hasattr(action, 'action_type'):
            action_type = action.action_type
        else:
            return 0

        # Base scores defining the heuristic's priorities
        scores = {
            ActionType.BUILD_CITY: 100,
            ActionType.BUILD_SETTLEMENT: 80,
            ActionType.BUY_DEV_CARD: 30,
            ActionType.BUILD_ROAD: 10,
            ActionType.PLAY_KNIGHT: 20,
            ActionType.PLAY_MONOPOLY: 20,
            ActionType.PLAY_YEAR_OF_PLENTY: 20,
            ActionType.PLAY_ROAD_BUILDING: 20,
            ActionType.MOVE_ROBBER: 15,
            ActionType.MARITIME_TRADE: 5,
            ActionType.END_TURN: 0,
            ActionType.ROLL: 50, # Always roll if available
            ActionType.DISCARD: 0, # Could be improved based on resource values
        }

        score = 0
        action_name = str(action_type).split('.')[-1]
        
        # Match by name to avoid potential enum identity issues across module imports
        for k, v in scores.items():
            if str(k).split('.')[-1] == action_name:
                score = v
                break

        # Tie-breaker: prefer anything over END_TURN if it has no base score
        if score == 0 and 'END_TURN' not in action_name:
            score = 1
            
        return score
