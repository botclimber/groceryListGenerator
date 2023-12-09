import gym 
from stable_baselines3 import PPO 
from stable_baselines3.common.vec_env import DummyVecEnv

import json
import numpy as np

FOLDER = "../../data/"
FILE = "continente_dataset_detailed_2023129.json"

class ReadDataset:

	def __init__(self, file):

		self.f = open(file, "r", encoding='utf-8')
		self.data = json.load(self.f)
		self.f.close()    

	def getData(self):
		return self.data

# Define the environment for grocery shopping
class GroceryEnvironment(gym.Env):
	USER_START_HAPPINESS = 50 # percentage | relies on user preferences
	USER_START_HEALTH = 100	# percentage | assume healthy user and how the products consumed affects the users health
	USER_TOTAL_MEALS = 14 # 1 week

	def __init__(self, budget_limit, user_preferences):
		super(GroceryEnvironment, self).__init__()
	
		self.userBudgetLimit = budget_limit
		
		self.userCurrentBudget = budget_limit
		self.userHappiness = USER_START_HAPPINESS
		self.userHealth = USER_START_HEALTH
		self.userMealNr = 1 

		# array of dictionaries with user preferrable items e.g. [{"product":"arroz", "brand":"continente"}]
		self.userPreferences = user_preferences

		# get all available products for buy
		refeicoes_faceis_instance = ReadDataset("{inFolder}{inFile}".format(inFolder=FOLDER, inFile=FILE))
		
		# sort list on product_name
		self.products = sorted(refeicoes_faceis_instance.getData()["refeicoes_faceis"], key=lambda d: d['product_name'])
		self.nr_products = len(products)
		
		# Actions: select a product
		self.action_space = gym.spaces.Discrete(nr_products)
		
		# Define the observation space
		self.observation_space = Dict(self.define_obs_state())
		
		print(self.observation_space)		

	def define_obs_state(self):
		return {
			'happiness': gym.spaces.Box(low=0, high=100, shape=(), dtype=float),
			'balance': gym.spaces.Box(low=0, high=self.userBudgetLimit, shape=(), dtype=float),
			'health': gym.spaces.Box(low=0, high=100, shape=(), dtype=float),
			'meal': gym.spaces.Box(low=0, high=USER_TOTAL_MEALS, shape=(), dtype=int),
			#'preferences': None TODO: define all possible preferences and five user only possibility to chose between
			# Add other attributes as needed
		}

	def get_observation(self):
		# Return the current observation based on user attributes
		observation = {
			'happiness': self.userHappiness,
			'balance': self.userCurrentBudget,
			'health': self.userHealth,
			'meal': self.userMealNr,
		}

		return observation

	def reset(self, random_budget, random_preferences = None):
		# random budget and preferences for training reasons
		self.userCurrentBudget = random_budget
		#self.userPreferences = random_preferences

		self.userHappiness = USER_START_HAPPINESS
		self.userHealth = USER_START_HEALTH
		self.userMealNr = 1

		# Return the initial observation
		return self.get_observation()

	def step(self, action):
		pass

	def render(self):
		pass

	def close(self):
		pass
