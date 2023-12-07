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
{
    "productName": string,
    "price": float,
    "quantity (unit/ grams/ liters)": float,
    "producer/brand": string,
    "nutritionScore": float,
    "protein": float, ?
    "calories": float, ?
    "preferenceRate": int,
    "countryOrigin": string,
    "sellerLocationName": string, e.g. (lidl, continente, pingo doce)" if from same seller better to avoid moving to different grocery store
    "foodType": string, (vegan, vegetarian, etc ...)
    (...) 
}
