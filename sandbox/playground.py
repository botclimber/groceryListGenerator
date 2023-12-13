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

