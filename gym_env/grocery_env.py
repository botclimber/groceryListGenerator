import gym 
from stable_baselines3 import PPO 
from stable_baselines3.common.vec_env import DummyVecEnv
import numpy as np

# Define the environment for grocery shopping
class GroceryEnvironment(gym.Env):
    def __init__(self, products, budget_limit):
        super(GroceryEnvironment, self).__init__()
        self.products = products  # List of products with their attributes
        self.budget_limit = budget_limit  # User's budget limit
        self.current_budget = self.budget_limit
        self.action_space = gym.spaces.Discrete(len(self.products))  # Actions: select a product
        self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(len(products),), dtype=np.float32)  # State space

    def reset(self):
        # Reset the environment, return initial state (list of available products)
        self.current_budget = self.budget_limit
        return np.array([product['price'] for product in self.products], dtype=np.float32)

    def step(self, action):
        # Execute action (select a product) and return next state, reward, done, info
        selected_product = self.products[action]
        if selected_product['price'] <= self.current_budget:
            self.current_budget -= selected_product['price']
            reward = selected_product['preferableRate']  # Adjust reward based on preferable rate or other criteria
        else:
            reward = -1  # Penalize selecting products exceeding the budget

        next_state = np.array([product['price'] for product in self.products], dtype=np.float32)
        done = self.current_budget <= 0  # End episode if budget is exhausted
        info = {}  # Additional information
        return next_state, reward, done, info


