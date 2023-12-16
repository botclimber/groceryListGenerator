import sys 
sys.path.append('../../gym_env')

import gym 

from stable_baselines3 import SAC 

import numpy as np
from grocery_env import GroceryEnvironment

env = GroceryEnvironment(debug_mode = True)

model = SAC.load("sac_mealPlanner_1000000")

userCurrentBudget = 50
userPreferences = [] # array of dictionaries with user preferrable items e.g. [{"product":"arroz", "brand":"continente"}] | "brand" in case of no brand preference just dont mention it, otherwise you can either chose one or more preferrable brands
age = 27
weight = 69
height = 175
gender = 1
physicalAct = 2

obs = env.reset(userCurrentBudget, userPreferences, age, weight, height, gender, physicalAct)
while True:
	# action, _states = model.predict(obs, deterministic=True)
	action, _states = model.predict(obs, deterministic=True)
	obs, reward, done, info = env.step(action)
	
	if done:	
		env.render()
		break
