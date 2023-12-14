import sys 
sys.path.append('../../gym_env')

import gym 

from stable_baselines3 import PPO 

import numpy as np
from grocery_env import GroceryEnvironment


env = GroceryEnvironment()

model = PPO.load("ppo_mealPlanner")

userCurrentBudget = 50
userPreferences = []
age = 27
weight = 69
height = 175
gender = 1
physicalAct = 2

obs = env.reset(userCurrentBudget, userPreferences, age, weight, height, gender, physicalAct)
while True:
	action, _states = model.predict(obs, deterministic=True)
	obs, reward, done, info = env.step(action)
	
	if done:	
		env.render()
		break
