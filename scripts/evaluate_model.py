import argparse
import time
import gymnasium as gym
import catanatron_gym
from stable_baselines3 import DQN

def evaluate(model_path: str, games: int):
    print(f"Loading environment 'catanatron-v1'...")
    
    env = gym.make("catanatron-v1")
    
    print(f"Loading model from {model_path}...")
    try:
        model = DQN.load(model_path, env=env)
    except Exception as e:
        print(f"Failed to load model. Ensure the path is correct and it is a zip file. Error: {e}")
        return

    print(f"\nEvaluating for {games} games...\n")
    
    wins = 0
    total_reward = 0
    
    for ep in range(games):
        obs, info = env.reset()
        done = False
        ep_reward = 0
        steps = 0
        
        while not done:
            # Let the model choose an action
            action, _states = model.predict(obs, deterministic=True)
            
            # Since DQN.predict might choose an invalid action in this specific environment setup
            # We explicitly check if it's valid, otherwise fallback or mask it.
            valid_actions = env.unwrapped.get_valid_actions()
            if action not in valid_actions:
                # Fallback if the DQN predicts an invalid action (common in naïve offline RL without action masking)
                import random
                action = random.choice(valid_actions)
                
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            ep_reward += reward
            steps += 1
            
        total_reward += ep_reward
        # Catanatron environments usually yield a large positive reward on win
        # We'll just define >0 as a win for this simple evaluation
        if ep_reward > 0:
            wins += 1
            print(f"Game {ep+1}: WON! (Reward: {ep_reward}, Steps: {steps})")
        else:
            print(f"Game {ep+1}: LOST. (Reward: {ep_reward}, Steps: {steps})")
            
    print(f"\n--- EVALUATION COMPLETE ---")
    print(f"Win Rate: {(wins/games)*100:.2f}% ({wins}/{games})")
    print(f"Average Reward: {total_reward/games:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a trained Catan model.")
    parser.add_argument("--model", type=str, default="smart_bot.zip", help="Path to the trained model (.zip)")
    parser.add_argument("--games", type=int, default=5, help="Number of evaluation games to play")
    
    args = parser.parse_args()
    evaluate(args.model, args.games)
