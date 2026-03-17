import argparse
import glob
import os
import pickle
import numpy as np

try:
    import gymnasium as gym
except ImportError:
    import gym
import catanatron_gym

from stable_baselines3 import PPO, DQN
from stable_baselines3.common.callbacks import CheckpointCallback

# Offline RL with SB3 is tricky because SB3 usually does online RL.
# We will create a custom environment that replays the dataset, or use DQNs replay buffer.
# For simplicity in this script, we'll just demonstrate loading the data and
# creating an empty model. True offline RL might require specific libraries (like d3rlpy) 
# or pre-loading the SB3 replay buffer.

def load_experiences(data_dir: str):
    print(f"Loading experiences from {data_dir}...")
    pkl_files = glob.glob(os.path.join(data_dir, "*.pkl"))
    if not pkl_files:
        print("No experience files found.")
        return []
        
    all_data = []
    for f in pkl_files:
        print(f"Loading {f}...")
        with open(f, "rb") as file:
            data = pickle.load(file)
            all_data.extend(data)
    
    print(f"Loaded {len(all_data)} total transitions.")
    return all_data

def train(data_dir: str, output_model: str, algo: str):
    transitions = load_experiences(data_dir)
    if not transitions:
        print("Cannot train without data.")
        return

    # In a real offline setting with SB3, you would populate the ReplayBuffer of a DQN
    # or use Behavior Cloning / Offline RL algorithms.
    # Here we will just initialize a DQN model and populate its buffer manually to show the pipeline.

    print("Initializing environment and model...")
    env = gym.make("catanatron-v1")
    
    # Initialize DQN model without exploring
    if algo.lower() == "dqn":
        model = DQN("MlpPolicy", env, verbose=1, learning_starts=0, buffer_size=len(transitions) + 1000)
        
        # Manually add to replay buffer
        print("Populating replay buffer...")
        # Note: Depending on SB3 version, populating buffer manually can require specific formats.
        # This is a basic outline.
        for index, t in enumerate(transitions):
            if hasattr(model.replay_buffer, 'add'):
                try:
                    # SB3 replay buffer requires: obs, next_obs, action, reward, done, info
                    model.replay_buffer.add(
                        t["obs"], 
                        t["next_obs"], 
                        np.array([t["action"]]), 
                        t["reward"], 
                        t["done"], 
                        [info] if 'info' in t else [{}]
                    )
                except Exception as e:
                    if index == 0:
                        print(f"Warning: Failed to add to buffer directly. Details: {e}")
                    pass
                    
        print("Starting offline training on buffer...")
        # Train for a certain number of timesteps
        model.learn(total_timesteps=len(transitions))
        
    elif algo.lower() == "ppo":
        print("PPO does not natively support offline replay buffer loading in SB3 in the same way. Skipping buffer population.")
        model = PPO("MlpPolicy", env, verbose=1)
        # Offline PPO requires something like Decision Transformer or behavior cloning.
    
    else:
        print(f"Algorithm {algo} not supported or implemented in this wrapper.")
        return

    print(f"Saving model to {output_model}...")
    model.save(output_model)
    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Stable-Baselines3 model offline.")
    parser.add_argument("--data_dir", type=str, default="data", help="Directory containing experience pickle files")
    parser.add_argument("--output_model", type=str, default="smart_bot", help="Path to save the resulting model zip")
    parser.add_argument("--algo", type=str, default="dqn", help="Which SB3 algorithm to use (dqn)")
    
    args = parser.parse_args()
    train(args.data_dir, args.output_model, args.algo)
