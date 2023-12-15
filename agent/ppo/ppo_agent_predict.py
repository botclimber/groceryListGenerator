import sys 
sys.path.append('../../gym_env')

import gym 

from stable_baselines3 import PPO 

import numpy as np
from grocery_env import GroceryEnvironment

env = GroceryEnvironment()

model = PPO.load("ppo_mealPlanner_2000000")

userCurrentBudget = 50
userPreferences = [] # array of dictionaries with user preferrable items e.g. [{"product":"arroz", "brand":"continente"}] | "brand" in case of no brand preference just dont mention it, otherwise you can either chose one or more preferrable brands
age = 27
weight = 69
height = 175
gender = 1
physicalAct = 2

obs = env.reset(userCurrentBudget, userPreferences, age, weight, height, gender, physicalAct)
while True:
	action, _states = model.predict(obs, deterministic=False)
	obs, reward, done, info = env.step(action)
	
	if done:	
		env.render()
		break
