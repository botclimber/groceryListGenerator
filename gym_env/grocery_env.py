import gym 
import re

from gym.spaces import Dict

import json
import numpy as np
import random

from lib import *

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
	USER_START_HAPPINESS = 100 # percentage | relies on user preferences
	USER_START_HEALTH = 100	# percentage | assume healthy user and how the products consumed affects the users health
	USER_TOTAL_MEALS = 14 # 1 week

	def __init__(self, debug_mode = False):
		super(GroceryEnvironment, self).__init__()

		self.debug_mode = debug_mode

		# get all available products for buy
		refeicoes_faceis_instance = ReadDataset("{inFolder}{inFile}".format(inFolder=FOLDER, inFile=FILE))
		
		# sort list on product_name
		self.sorted_products_by_name = sorted(refeicoes_faceis_instance.getData()["refeicoes_rapidas"], key=lambda d: d['prod_name'])
		totalProducts = len(self.sorted_products_by_name)

		# filter only on products with nutrition information
		self.products = [product for product in self.sorted_products_by_name if len(product["prod_nutri_info"][2]) > 0]
		self.nr_use_products = len(self.products)
		
		self.message(f"TOTAL PRODUCTS: {totalProducts}")
		self.message(f"AVAILABLE PRODUCTS: {self.nr_use_products}")

		# Actions: select a product
		# self.action_space = gym.spaces.Discrete(self.nr_use_products)
		self.action_space = gym.spaces.Box(low=0, high=self.nr_use_products - 1, shape=(1,), dtype=np.int64)
		
		# Define the observation space
		self.observation_space = Dict(self.define_obs_state())		

	def message(self, txt):
		if self.debug_mode:
			print(txt)

	def define_obs_state(self):
		return {
			'happiness': gym.spaces.Box(low=0, high=100, shape=(1,), dtype=float),
			'balance': gym.spaces.Box(low=0, high=np.inf, shape=(1,), dtype=float),
			'health': gym.spaces.Box(low=0, high=100, shape=(1,), dtype=float),
			'meal': gym.spaces.Box(low=0, high=self.USER_TOTAL_MEALS, shape=(1,), dtype=int),
			'age': gym.spaces.Box(low=0, high=110, shape=(1,), dtype=int),
			'weight': gym.spaces.Box(low=0, high=np.inf, shape=(1,), dtype=int),
			'height': gym.spaces.Box(low=0, high=np.inf, shape=(1,), dtype=int),
			'gender': gym.spaces.Box(low=0, high=1, shape=(1,), dtype=int),
			'physicalAct': gym.spaces.Box(low=0, high=10, shape=(1,), dtype=int)
			#'preferences': None TODO: define all possible preferences and five user only possibility to chose between
			# Add other attributes as needed
		}

	def get_observation(self):
		# Return the current observation based on user attributes
		observation = {
			'happiness': np.array([self.userHappiness]),
			'balance': np.array([self.userCurrentBudget]),
			'health': np.array([self.userHealth]),
			'meal': np.array([self.userMealNr]),
			'age': np.array([self.age]),
			'weight': np.array([self.weight]),
			'height': np.array([self.height]), 
			'gender': np.array([self.gender]),
			'physicalAct': np.array([self.physicalAct])
		}

		return observation

	def reset(self, u_budget = None, u_preferences = None, age = None, weight = None, height = None, gender = None, physicalAct = None):

		# user info
		# random budget and preferences for training reasons
		self.userCurrentBudget = random.randint(20, 250) if u_budget is None else u_budget
		self.age = random.randint(1, 110) if age is None else age
		self.gender = random.randint(0, 1) if gender is None else gender # 0 - women | 1 - men
		self.weight = random.randint(40, 200) if weight is None else weight
		self.height = random.randint(100, 210) if height is None else height # in cm
		self.physicalAct = random.randint(0, 10) if physicalAct is None else physicalAct # from 0 to 10		

		# array of dictionaries with user preferrable items e.g. [{"product":"arroz", "brand":"continente"}] | "brand" can also be an array containing multiple preferable brands
		self.userPreferences = [] if u_preferences is None else u_preferences

		self.startedBudget = self.userCurrentBudget

		# nutri meals info
		self.calories = 0 # kcal (Quilocaloria PT)
		self.lipids = 0 # g (grams)
		self.carbos = 0 # g (grams)
		self.fiber = 0 # g (grams)
		self.protein = 0 # g (grams)
		self.salt = 0 # g (grams)

		self.userHappiness = self.USER_START_HAPPINESS
		self.userHealth = self.USER_START_HEALTH
		self.userMealNr = 1

		self.selectedActions = []
		self.totalReward = 0

		self.message(self.get_observation())
		return self.get_observation()

	def getNutrients(self, dict):
		
		fromListToDict = {}
		for n in dict:
			key = list(n.keys())[0]
			fromListToDict[key] = {"value": n[key], "unit": n["unit"]}

		return fromListToDict

	def normalize(self, value, min_val, max_val):
		return (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5

	# TODO: give bad reward in case of selecting same action
	def compute_reward(self, done):
		# Combine rewards with weights if needed
		self.message("\t\tREWARD:")

		weights = {
			"happiness" : 0.0,
			"health": 0.4,
			"budget_limit": 0.6 
		}

		if done and (self.userMealNr < 14 or self.userCurrentBudget < 0):
			reward = -1

		else:
			# Normalizing state variables
			normalized_health = self.normalize(self.userHealth, 0, self.USER_START_HEALTH)
			normalized_happiness = self.normalize(self.userHappiness, 0, self.USER_START_HAPPINESS)
			normalized_budget = self.normalize(self.userCurrentBudget, 0, self.startedBudget)

			self.message(f"\t\t\tNORMALIZED HAPPINESS: {normalized_happiness}")
			self.message(f"\t\t\tNORMALIZED HEALTH: {normalized_health}")
			self.message(f"\t\t\tNORMALIZED LIMIT_BUDGET: {normalized_budget}")

			self.message(f" SELECTE DACTIONS: {self.selectedActions} | {len(np.unique(self.selectedActions))}")
			
			reward = round(( (normalized_health * weights["health"]) + (normalized_happiness * weights["happiness"]) + (normalized_budget * weights["budget_limit"])) * len(np.unique(self.selectedActions)), 2)

		self.totalReward += reward
		return reward

	# return void
	def compute_observation(self, name, brand, cost, caloriesDiff = None, lipidsDiff = None, carbosDiff = None, fiberDiff = None, proteinDiff = None, saltDiff = None):
			
		# Compute User Health
		self.userHealth += round(self.compute_userHealth(caloriesDiff, lipidsDiff, carbosDiff, fiberDiff, proteinDiff, saltDiff), 2)
		
		# Compute User Happiness
		self.userHappiness += round(self.compute_userHappiness(name, brand), 2)

		self.stabilizer()

		self.userCurrentBudget -= round(cost, 2)

	def compute_userHappiness(self, name, brand):
		if not self.userPreferences:
			return 0

		happinessConstant = 100 / self.USER_TOTAL_MEALS

		for preference in self.userPreferences:
			prod_to_be_found = preference["product"].lower()
			
			try:
				brands_to_be_found = preference["brand"]
			except:
				brands_to_be_found = None

			if isinstance(brands_to_be_found, str):
				brands_to_be_found = [brands_to_be_found]  # Convert to list if it's a string

			if prod_to_be_found in name.lower():
				self.message(f"\n\t\tProduct name '{prod_to_be_found}' found in preferences for product '{name}'")

				if brands_to_be_found is not None and any(b.lower() in brand.lower() for b in brands_to_be_found):
					self.message(f"\t\tBoth product '{prod_to_be_found}' and brand '{brand}' found in preferences for product '{name}'")
					return happinessConstant

				self.message(f"\t\tBrand '{brand}' not found in preferences for product '{name}'")
				return happinessConstant / 2

		self.message(f"\n\t\tProduct name '{prod_to_be_found}' not found in preferences for product '{name}'")
		return -happinessConstant                                                                  
		
	
	def compute_userHealth(self, diffCalories, diffLipids, diffCarbos, diffFiber, diffProtein, diffSalt):
		nutrient_diffs = [diffCalories, diffLipids, diffCarbos, diffFiber, diffProtein, diffSalt]
		
		self.message(f"\n\t\tNUTRIENTS DIFF {nutrient_diffs}")
		# Define nutrient weights
		weights = {
			"calories": 0.4,
			"lipids": 0.1,
			"carbos": 0.1,
			"fiber": 0.15,
			"protein": 0.15,
			"salt": 0.05
		}

		# Calculate nutrient impacts considering weights
		nutrient_impact = [diffValue * weights[key] for key, diffValue in zip(weights.keys(), nutrient_diffs)]

		self.message(f"\t\tNUTRIENT_IMPACT: {nutrient_impact}")

		# Compute overall health impact
		health_impact = sum(nutr if nutr < 0 else -nutr for nutr in nutrient_impact) / self.USER_START_HEALTH
		self.message(f"\t\tHealth Impact is: {health_impact}")

		return health_impact

	def stabilizer(self):

		if(self.userHealth > 100): self.userHealth = self.USER_START_HEALTH
		if(self.userHealth < 0): self.userHealth = 0

		if(self.userHappiness > 100): self.userHappiness = self.USER_START_HAPPINESS
		if(self.userHappiness < 0): self.userHappiness = 0

	def get_parsed_value(self, dictionary, key):
		try:
			return float(dictionary[key]["value"]), dictionary[key]["unit"]
		except (KeyError, TypeError):
			return 0, None

	def get_quantity(self, prod_qty):
		defaultMidTerm = 200

		patternNrUnit = r'\b\d+\s*gr\b'
		patternNr = r'\d+'

		matches = re.findall(patternNrUnit, prod_qty)
		self.message(f"\n\t\t NR of QUANTITIES FOUND ({len(matches)}) \n")

		if not matches:
			self.message(f"\n\t\t Quantity not found, using default {defaultMidTerm}g \n")
			return defaultMidTerm
		
		else:
			qty = float(re.findall(patternNr, matches[0])[0])
			self.message(f"\n\t\t Found {qty}g \n")
			return qty

	def step(self, action):
		'''
		enforce Agent to not chose always the same action
		delay reward to be sent only when step is even which represents 2 meals 1 day
		'''
		action = int(action[0])
		self.message(f" \n ------ Currently on Meal nr {self.userMealNr} with action nr {action}  ------ \n")
		self.selectedActions.append(action)

		done = False
		
		sel_product = self.products[action]
		
		prod_qty = self.get_quantity(sel_product["prod_qty"])
		nutri_portion = float(sel_product["prod_nutri_info"][0])
		qtyByPortion = prod_qty / nutri_portion

		nutritients = self.getNutrients(sel_product["prod_nutri_info"][2][1:])

		parsed_price = float(sel_product["prod_price"])
		
		energy_amount, unit_energy = self.get_parsed_value(nutritients, "energia")
		lipids_amount, unit_lipids = self.get_parsed_value(nutritients, "lípidos")
		carbos_amount, unit_carbos = self.get_parsed_value(nutritients, "hidratos de carbono")
		fiber_amount, unit_fiber = self.get_parsed_value(nutritients, "fibra")
		protein_amount, unit_protein = self.get_parsed_value(nutritients, "proteínas")
		salt_amount, unit_salt = self.get_parsed_value(nutritients, "sal")

		parsed_energy = qtyByPortion * energy_amount
		parsed_lipids = qtyByPortion * lipids_amount
		parsed_carbos = qtyByPortion * carbos_amount
		parsed_fiber = qtyByPortion * fiber_amount
		parsed_protein = qtyByPortion * protein_amount
		parsed_salt = qtyByPortion * salt_amount

		self.calories += parsed_energy
		self.lipids += parsed_lipids
		self.carbos += parsed_carbos
		self.fiber += parsed_fiber
		self.protein += parsed_protein
		self.salt += parsed_salt
	
		nrc = NRC(self.age, self.gender, self.weight, self.height, self.physicalAct)
		tdee = round(nrc.calcTDEE(), 3)

		self.message(f"\t\t Selected Product: ")
		self.message(f"\t\t\t NAME: {sel_product['prod_name']}")
		self.message(f"\t\t\t QUANTITY: {prod_qty} ")
		self.message(f"\t\t\t PRICE: {parsed_price} ")
		self.message(f"\t\t\t NUTRITION INFO (b/Qty): ")
		self.message(f"\t\t\t\t Energy (kcal): {parsed_energy} ")
		self.message(f"\t\t\t\t Lipids (g): {parsed_lipids} ")
		self.message(f"\t\t\t\t Carbos (g): {parsed_carbos} ")
		self.message(f"\t\t\t\t Fiber (g): {parsed_fiber}")
		self.message(f"\t\t\t\t Protein (g): {parsed_protein}")
		self.message(f"\t\t\t\t Salt (g): {parsed_salt}")

		self.message(f"\t\tTOTAL DAILY ENERGY EXPENDITURE (TDEE) is {tdee}")

		self.message(f"\t\tNutrition Information: Calories: {parsed_energy} | Lipids: {parsed_lipids} | Carbos: {parsed_carbos} | Fiber: {parsed_fiber} | Protein: {parsed_protein} | Salt: {parsed_salt}")

		energyDiff = EnergyPerDay(parsed_energy, unit_energy).compWithDailyRec(tdee)
		lipidsDiff = LipidsPerDay(parsed_lipids, unit_lipids, parsed_energy).compWithDailyRec()
		carbosDiff = CarbonHidratsPerDay(parsed_carbos, unit_carbos, parsed_energy).compWithDailyRec()
		fiberDiff = FiberPerDay(parsed_fiber, unit_fiber).compWithDailyRec()
		proteinDiff = ProteinPerDay(parsed_protein, unit_protein, self.weight, self.physicalAct).compWithDailyRec()
		saltDiff = SaltPerDay(parsed_salt, unit_salt).compWithDailyRec()

		self.message(f"\t\tCOMPUTED DAILY NUTRITION DIFFs -> Energy: {energyDiff} | LIPIDS: {lipidsDiff} | CARBOS: {carbosDiff} | FIBER: {fiberDiff} | PROTEIN:{proteinDiff} | SALT: {saltDiff}")

		self.compute_observation(sel_product["prod_name"], sel_product["prod_brand"], parsed_price, energyDiff, lipidsDiff, carbosDiff, fiberDiff, proteinDiff, saltDiff)

		if(self.userMealNr >= self.USER_TOTAL_MEALS or self.userCurrentBudget <= 0): 
			done = True
			self.message(f'\n\t\tTOTAL NUTRIENTS CONSUMED -> Energy: {self.calories} | LIPIDS: {self.lipids} | CARBOS: {self.carbos} | FIBER: {self.fiber} | PROTEIN: {self.protein} | SALT: {self.salt}')
			self.message(f"\t\tACTION HISTORY: [{self.selectedActions}]")
			self.message(f"\t\tTotal money spent: [{(self.startedBudget) - self.userCurrentBudget}]")

		observation = self.get_observation()
		reward = self.compute_reward(done)

		self.message(f"\n\t\t REWARD: ({reward})")
		self.message(f"\t\t TOTAL REWARD: ({self.totalReward}) \n")
		self.message(f"\n\t\t OBSERVATION: ({observation}) \n")

		self.userMealNr += 1
		return observation, reward, done, {}

	def render(self):
		print("\n\n\t\t ************ RESULT ************ \n\n")
		print(f"\t\tUser Info: Gender: {'Men' if self.gender == 1 else 'Women'} | Age: {self.age} years | Weight: {self.weight}kg | Height: {self.height / 100}m | Physical Activity: {self.physicalAct}\n\n")

		for index, action in enumerate(self.selectedActions):
			print(f"\t\t\t{index+1}. \t{self.products[action]['prod_name']} | {self.products[action]['prod_brand']} | {self.products[action]['prod_price']} | {self.products[action]['prod_qty']}")
		
		print(f"\n\t\t {round((self.startedBudget) - self.userCurrentBudget, 2)} spent from given {self.startedBudget} budget limit.")
		print(f'\t\tTOTAL NUTRIENTS CONSUMED -> Energy: {self.calories} | LIPIDS: {self.lipids} | CARBOS: {self.carbos} | FIBER: {self.fiber} | PROTEIN: {self.protein} | SALT: {self.salt}.')
		print(f'\n\t\t TOTAL REWARD: {self.totalReward}')

	def close(self):
		pass
