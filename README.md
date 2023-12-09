# CURRENT IDEA

AI meal planner

---
@DEPRECATED
# AI Grocery list generator
this is a skeleton for an experiment, where an AI trained with RL trained for a specific country, tries to create a suitable grocery list based on budget limit, nutrition score (health), diet preferences (vegan, vegetarian, etc ...)

Advantages:
- Personalized Recommendations: The AI can tailor suggestions based on individual preferences, dietary needs, budget constraints, and other factors.

- Time and Effort Saving: It can save time and effort by automating the process of creating shopping lists, ensuring essential items are included and unnecessary ones are excluded.

- Budget Optimization: The AI can assist in optimizing the grocery list within specified budget limits, helping users make cost-effective choices.

- Healthy Choices: By considering nutrition scores and user preferences, the AI can promote healthier food choices.

- Adaptability: It can adapt to changes in preferences or dietary requirements over time, providing flexible recommendations.

- Learning and Improvement: With reinforcement learning, the AI can continuously learn from user feedback, enhancing the quality of recommendations.

- Convenience and Accessibility: Users can access and receive grocery recommendations at their convenience, potentially through mobile apps or web interfaces.

--- 
dataset format:
{}

--
webscrapping:
** dataThief ** is where webscrapping functionality is located. At the moment is only getting data from continente/mercearia with scrapy to get all generic existing products and an independent script located still in the spiders folder to get more detailed information about download products. 

Idea is to scale this to get also other products as e.g. "Peixaria e Talho", "Lacticinios e Ovos", "Frutas e Legumes", etc ...

- continente
    - best data provider
- pingo doce ?