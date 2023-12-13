'''
data = [
    {"energia": "711.28", "unit": "Quilojoule"},
    {"energia": "170.0", "unit": "Quilocaloria"},
    {"lípidos": "15.5", "unit": "Grama"},
    {"lípidos > saturados": "3.2", "unit": "Grama"},
    {"hidratos de carbono": "4.3", "unit": "Grama"},
    {"hidratos de carbono > açúcares": "1.3", "unit": "Grama"},
    {"fibra": "3.1", "unit": "Grama"},
    {"proteínas": "1.9", "unit": "Grama"},
    {"sal": "0.87", "unit": "Grama"}
][1:]

nutrition_dict = {}

for item in data:
	
	key = list(item.keys())[0]	
	nutrition_dict[key] = {"value": item[key], "unit": item["unit"]}
	print(nutrition_dict)
'''

'''
user_preferences = [{"product":"arroz", "brand":["continente", "deluxe"]},{"product":"massa com gambas", "brand":"continente"},{"product":"bacalhau com natas", "brand":"deluxe"}]

name = "Arroz de cabidela"
brand = "continente"

for x in user_preferences:
	findInProduct = name.lower()
	prodToBeFound = x["product"].lower()

	findInBrand = brand.lower()
	brandToBeFound = x["brand"] 
	
	#if(whereToFind.find(whatToBeFound) != -1):
	#	print("prod ",whatToBeFound," found in ",whereToFind)
	#else:
	#	print("prod ",whatToBeFound," not found in ",whereToFind)

'''
user_preferences = [
    {"product": "arroz", "brand": ["continente", "deluxe"]},
    {"product": "massa com gambas", "brand": "continente"},
    {"product": "bacalhau com natas", "brand": "deluxe"}
]

name = "Arroz de cabidela"
brand = "continente"
for preference in user_preferences:
			prod_to_be_found = preference["product"].lower()
			brands_to_be_found = preference["brand"]

			if isinstance(brands_to_be_found, str):
				brands_to_be_found = [brands_to_be_found]  # Convert to list if it's a string
			
			if prod_to_be_found in name.lower():
				print(f"Product name '{prod_to_be_found}' found in preferences for product '{name}'")
				# 2/3 medium happy

				if any(brand.lower() == b.lower() for b in brands_to_be_found):
					print(f"Both product '{prod_to_be_found}' and brand '{brand}' found in preferences for product '{name}'")
					# 3/3 super happy

				else:
					print(f"Brand '{brand}' not found in preferences for product '{name}'")
					# 1/3 happy

			else:
				print(f"Product name '{prod_to_be_found}' not found in preferences for product '{name}'")
				# no happy    
