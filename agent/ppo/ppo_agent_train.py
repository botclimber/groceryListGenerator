import sys
sys.path.append('../../gym_env')

import gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback

import numpy as np
from grocery_env import GroceryEnvironment

from stable_baselines3.common.noise import NormalActionNoise

env = GroceryEnvironment()

# Define a callback to log the mean episode reward and mean episode length
eval_callback = EvalCallback(
    env,
    callback_on_new_best=None,
    eval_freq=5000,  # Log every X steps
    deterministic=True,
    render=False,
)

# pi = [32, 32] policy network of 2 hidden layers with 32 neurons each (maps states or obs to actions)
# vf = [32, 32] value function of 2 hidden layers with 32 neurons each (estimates the value of being in a particular state or following a particular action in a state)
#policy_kwargs = dict(activation_fn=th.nn.ReLU,net_arch=dict(pi=[32, 32], vf=[32, 32]))

# Initialize and train the RL agent | TODO: explain each parameter
learn_steps = 10000000
model = PPO("MultiInputPolicy",
            env,
            verbose=1,
            tensorboard_log=f"./logs/ppo_mealPlanner_{learn_steps}/",
            ent_coef = 0.01,
            learning_rate = 0.001,
            clip_range = 0.3,
            #use_sde = True,
            #sde_sample_freq = 16,
            gae_lambda = 0.97)

model.learn(total_timesteps=learn_steps, callback=eval_callback)

# Save the trained model
model.save(f"ppo_mealPlanner_{learn_steps}") # to continue training load pre-saved model
