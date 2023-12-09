import gym 
from stable_baselines3 import PPO 
from stable_baselines3.common.vec_env import DummyVecEnv
import numpy as np

# Load products from file and transform into an useful/required dataset 
class ProductsLT:
'''
folder and file are fixed, so user just need to change file in one place
'''
	FOLDER = "../data/"
	FILENAME = "data.json"

	def __init__(self):
		# open file
		# read from file
		# transform data read
		pass
	
	def __transform(self):
		'''
		Dict Format
			{}
		'''
		# transform data upload from file
		# return Dict
		pass	

	# return transformed products
	def getProducts(self):
		#return products 
		pass

# Define the environment for grocery shopping
class GroceryEnvironment(gym.Env):
	USER_START_HAPPINESS = 50 # percentage | relies on user preferences
	USER_START_HEALTH = 100	# percentage | assume healthy user and how the products consumed affects the users health

	def __init__(self, budget_limit):
		super(GroceryEnvironment, self).__init__()
	
		self.userBudgetLimit = budget_limit
		
		self.userCurrentBudget = budget_limit
		self.userHappiness = USER_START_HAPPINESS 
		self.userHealth = USER_START_HEALTH

		# get all available products for buy
		self.products = ProductsLT().getProducts() 
		self.nr_products = len(products)
		
		self.action_space = gym.spaces.Discrete(nr_products)  # Actions: select a product
	
		# product info format	
		self.product_info = self._define_product_info()
		
		self.observation_keys = self.define_obs_state().keys() # user state
		
		# Define the observation space
		self.observation_space = Dict(self.define_user_state())
		
		print(self.observation_space)		

	def define_obs_state(self):
		return {
			'happiness': gym.spaces.Box(low=0, high=100, shape=(), dtype=float),
			'balance': gym.spaces.Box(low=0, high=self.userBudgetLimit, shape=(), dtype=float),
			'health': gym.spaces.Box(low=0, high=100, shape=(), dtype=float),
			# Add other attributes as needed
		}

	def get_observation(self):
		# Return the current observation based on user attributes
		observation = {
			'happiness': self.userHappiness,
			'balance': self.userCurrentBudget,
			'health': self.userHealth,
		}

		return observation

	def reset(self):
		self.userHappiness = USER_START_HAPPINESS
		self.userCurrentBudget = self.userBudgetLimit 
		self.userHealth = USER_START_HEALTH

		# Return the initial observation
		return self.get_observation() 

	def step(self, action):
		# Validate the action
		assert self.action_space.contains(action), f"Invalid action: {action}"

		# Assume action is the index of the selected product
		selected_product = self.products[action]

		# Update user attributes based on the selected product (modify this based on your logic)
		self.userHappiness -= 10  # Example: Reduce happiness by 10 for simplicity
		self.userHealth += 5  # Example: Increase health by 5 for simplicity
		self.userCurrentBudget -= selected_product['price']  # Reduce budget based on selected product price

		# Define the new observation
		new_observation = self._get_observation()

		# Define the reward (modify this based on your reward logic)
		reward = -selected_product['price']  # Negative of the price as a simple reward

		# Check if the episode is done based on a termination condition (modify this based on your criteria)
		done = self.userCurrentBudget <= 0  # Episode ends if the budget is exhausted

		# Additional information (optional)
		info = {"selected_product": selected_product}

		return new_observation, reward, done, info

	def render(self):
		pass

	def close(self):
		pass
