import sys
sys.path.append('../gym_env')

import gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import numpy as np
from grocery_env import GroceryEnvironment

# define dataset
products_data = [
    {"product_name": "Apple", "price": 1, "quantity": 1, "origin/producer": "Local", "nutritionScore": 8, "protein": 1, "calories": 50, "preferableRate": 0.8},
    # Add more products here...
]

# Define user's budget limit
budget_limit = 20.0  # Replace with user's budget

# Create the environment and wrap it as a vectorized environment
env = GroceryEnvironment(budget_limit)
vec_env = DummyVecEnv([lambda: env])

# Initialize and train the RL agent
model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=5000)

# Save the trained model
model.save("grocery_rl_model")
