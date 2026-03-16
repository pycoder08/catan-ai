try:
    import gymnasium as gym
except ImportError:
    import gym
import catanatron_gym

def explore():
    print("Loading Environment...")
    
    env_name = "catanatron-v1"
    print(f"\nAttempting to make: {env_name}")
    
    try:
        env = gym.make(env_name)
    except Exception as e:
        print(f"ERROR: Failed to make environment {env_name}. Details: {e}")
        return
        
    # 1. Inspect spaces
    print("\n--- SPACES ---")
    print(f"Observation Space: {env.observation_space}")
    print(f"Action Space:      {env.action_space}")
    
    # 2. Reset and get initial observation
    obs = env.reset()
    if isinstance(obs, tuple) and len(obs) == 2:
        # Gym >=0.26 usually returns (obs, info)
        obs, info = obs
    print("\n--- INITIAL OBSERVATION ---")
    print(f"Shape: {obs.shape if hasattr(obs, 'shape') else type(obs)}")
    
    # 3. Take a random action
    print("\n--- TAKING ONE RANDOM ACTION ---")
    action = env.action_space.sample()
    
    step_result = env.step(action)
    
    if len(step_result) == 4:
        next_obs, reward, done, info = step_result
        print(f"Reward: {reward}, Done: {done}")
    else:
        next_obs, reward, terminated, truncated, info = step_result
        print(f"Reward: {reward}, Terminated: {terminated}, Truncated: {truncated}")
        
    print(f"New Observation Shape: {next_obs.shape if hasattr(next_obs, 'shape') else type(next_obs)}")

if __name__ == "__main__":
    explore()
