import gym 
from stable_baselines3 import PPO 
from stable_baselines3.common.vec_env import DummyVecEnv

import json
import numpy as np
import random

import lib

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

	def __init__(self, budget_limit, user_preferences, age, weight, height, gender, physicalAct):
		super(GroceryEnvironment, self).__init__()
	
		# user info
		self.userBudgetLimit = budget_limit
		self.age = age
		self.weight = weight
		self.gender = gender
		self.height = height
		self.physicalAct = physicalAct

		# nutri meals info
		self.calories = 0 # kcal (Quilocaloria PT)
		self.lipids = 0 # g (grams)
		self.carbos = 0 # g (grams)
		self.fiber = 0 # g (grams)
		self.protein = 0 # g (grams)
		self.salt = 0 # g (grams)
	
		# real time data
		self.userCurrentBudget = budget_limit
		self.userHappiness = USER_START_HAPPINESS
		self.userHealth = USER_START_HEALTH
		self.userMealNr = 1 

		# historical data
		self.selectedActions = []

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
			'age': gym.spaces.Box(low=0, high=120, shape=(), dtype=int),
			'weight': gym.spaces.Box(low=0, high=np.inf, shape=(), dtype=int),
			'height': gym.spaces.Box(low=0, high=np.inf, shape=(), dtype=int),
			'gender': gym.spaces.Box(low=0, high=1, shape=(), dtype=int),
			'physicalAct': gym.spaces.Box(low=0, high=10, shape=(), dtype=int),
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
			'age': self.age,
			'weight': self.weight,
			'height': self.height, 
			'gender': self.gender,
			'physicalAct': self.physicalAct
		}

		return observation

	def reset(self):
		# random budget and preferences for training reasons
		self.userCurrentBudget = random_budget
		
		self.age = random.randint(1, 120) 
		self.gender = random.randint(0, 1)
		self.weight = random.randint(40, 200)
		self.height = round(random.uniform(1, 2.10),2)
		self.physicalAct = random.randint(0, 10)		

		#self.userPreferences = random_preferences

		self.userHappiness = USER_START_HAPPINESS
		self.userHealth = USER_START_HEALTH
		self.userMealNr = 1

		# Return the initial observation
		return self.get_observation()

	def getNutrients(self, dict):
		
		fromListToDict = {}
		for n in dict:
			key = list(n.keys())[0]
			fromListToDict[key] = {"value": n[key], "unit": n["unit"]}

		return fromListToDict

	def reward(self):
		pass


	def step(self, action):
		'''
		enforce Agent to not chose always the same action
		delay reward to be sent only when step is even which represents 2 meals 1 day
		'''
		sel_product = self.products[action]
		nutritients = self.getNutrients(self.products["prod_nutri_info"][2][1:])
	
		nrc = NRC(self.age, self.gender, self.weight, self.height, self.physicalAct)

		bmr = nrc.calcBMR()
		tdee = nrc.calcTDEE()

		if(self.meals % 2 == 0):
			self.calories += nutritients["energia"]["value"]
			self.lipids += nutritients["lípidos"]["value"]
			self.carbos += nutritients["hidratos de carbono"]["value"]
			self.fiber += nutritients["fibra"]["value"]
			self.protein += nutritients["proteínas"]["value"]
			self.salt += nutritients["sal"]["value"]

		else:
			self.calories = nutritients["energia"]["value"]
			self.lipids = nutritients["lípidos"]["value"]
			self.carbos = nutritients["hidratos de carbono"]["value"]
			self.fiber = nutritients["fibra"]["value"]
			self.protein = nutritients["proteínas"]["value"]
			self.salt = nutritients["sal"]["value"]


		pass

	def render(self):
		pass

	def close(self):
		pass
