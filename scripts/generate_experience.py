import argparse
import os
import pickle
import time
from datetime import datetime

try:
    import gymnasium as gym
except ImportError:
    import gym
import catanatron_gym

def collect_experience(episodes: int, output_dir: str):
    """
    Simulates episodes of Catan using a random agent and records experience tuples.
    (observation, action, reward, next_observation, done)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"experience_{timestamp}.pkl")

    print(f"Initializing 'catanatron-v1' environment...")
    try:
        env = gym.make("catanatron-v1")
    except Exception as e:
        print(f"ERROR: Failed to make environment. Details: {e}")
        return

    experiences = []
    total_steps = 0
    start_time = time.time()

    print(f"Starting data collection for {episodes} episodes...")

    for ep in range(episodes):
        obs = env.reset()
        if isinstance(obs, tuple) and len(obs) == 2:
            obs, info = obs  # Gymnasium compatibility
            
        done = False
        ep_reward = 0
        ep_steps = 0
        
        while not done:
            # Sample random action from valid action space
            valid_actions = env.unwrapped.get_valid_actions()
            import random
            action = random.choice(valid_actions)
            
            step_result = env.step(action)
            if len(step_result) == 4:
                next_obs, reward, done_flag, info = step_result
                terminated, truncated = done_flag, False
            else:
                next_obs, reward, terminated, truncated, info = step_result
                
            done = terminated or truncated

            # Store the tuple
            experiences.append({
                "obs": obs,
                "action": action,
                "reward": reward,
                "next_obs": next_obs,
                "done": done
            })

            obs = next_obs
            ep_reward += reward
            ep_steps += 1
            total_steps += 1

        if (ep + 1) % 10 == 0 or (ep + 1) == episodes:
            print(f"Episode {ep + 1}/{episodes} completed. Episode Steps: {ep_steps}. Total Experiences: {len(experiences)}")

    # Save to disk
    print(f"\nSaving {len(experiences)} transitions to {output_path}...")
    with open(output_path, "wb") as f:
        pickle.dump(experiences, f)
    
    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate reinforcement learning experience for Catan.")
    parser.add_argument("--episodes", type=int, default=1, help="Number of games to simulate")
    parser.add_argument("--output_dir", type=str, default="data", help="Directory to save the pickle files")
    
    args = parser.parse_args()
    collect_experience(args.episodes, args.output_dir)
