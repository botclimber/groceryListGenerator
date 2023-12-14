import sys
sys.path.append('../../gym_env')

import gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback

import numpy as np
from grocery_env import GroceryEnvironment

env = GroceryEnvironment()

# Define a callback to log the mean episode reward and mean episode length
eval_callback = EvalCallback(
    env,
    callback_on_new_best=None,
    best_model_save_path='./logs/best_ones/ppo_mealPlanner_tensorboard/',
    log_path='./logs/ppo_mealPlanner_tensorboard/',
    eval_freq=1000,  # Log every 1000 steps
    deterministic=True,
    render=False,
)

# Initialize and train the RL agent
model = PPO("MultiInputPolicy", env, verbose=1,tensorboard_log="./logs/ppo_mealPlanner/")
model.learn(total_timesteps=500000, callback=eval_callback)

# Save the trained model
model.save("ppo_mealPlanner")
