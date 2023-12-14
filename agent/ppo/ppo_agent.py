import sys
sys.path.append('../../gym_env')

import gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

import numpy as np
from grocery_env import GroceryEnvironment

budget_limit = 200
user_preferences = []
age = 27
weight = 69
gender = 1
height = 175
physicalAct = 2

# Create the environment and wrap it as a vectorized environment
env = GroceryEnvironment(budget_limit, user_preferences, age, weight, height, gender, physicalAct)
vec_env = DummyVecEnv([lambda: env])

# Initialize and train the RL agent
model = PPO("MultiInputPolicy", vec_env, verbose=1)
model.learn(total_timesteps=100000)

# Save the trained model
model.save("mealPlanner_rl_model")
