import gym
import catanatron_gym

def explore():
    print("Loading Environment...")
    
    # Debug: see what is actually registered
    from gym.envs.registration import registry
    print("\nAvailable Catan environments:")
    catan_envs = [env_id for env_id in registry.env_specs.keys() if 'catan' in env_id.lower()]
    print(catan_envs)
    
    if not catan_envs:
        print("ERROR: No catan environments found in registry! Did you import catanatron_gym?")
        return
        
    env_name = catan_envs[0]
    print(f"\nAttempting to make: {env_name}")
    env = gym.make(env_name)
    
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
    print(obs)
    
    # 3. Take a random action
    print("\n--- TAKING ONE RANDOM ACTION ---")
    action = env.action_space.sample()
    
    # gym <=0.25 returns obs, reward, done, info
    # gym >=0.26 returns obs, reward, terminated, truncated, info
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
