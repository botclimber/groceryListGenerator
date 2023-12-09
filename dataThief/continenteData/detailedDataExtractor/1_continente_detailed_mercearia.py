from requests_html import HTMLSession
import json
import numpy as np
import datetime

from commonReader import ReadFromJSON

time_now = datetime.datetime.now()
currentDate = time_now.year+time_now.month+time_now.day

data = ReadFromJSON("../data/mercearia/continente_dataset_generic_"+currentDate+".json").getData()

s = HTMLSession()

with open("../data/mercearia/generated/continente_dataset_detailed_"+currentDate+".json", "a", encoding="utf-8") as f:
	for x in data:
		print("Handling product ["+x["prod_name"]+"]:")
		# print(x)
		
		r = s.get(x["prod_link"])
		r.html.render(sleep=1)	

		portionElement = r.html.xpath("//div[@class='serving-size']/p[@class='mb-20']", first=True)
		unitElement = r.html.xpath("//div[@class='serving-size--uom']/p[@class='mb-20']", first=True)
		products = r.html.xpath("//div[@class='nutriInfo-details col-4 col-sm nutrients-cell']")
		
		if( not portionElement and not unitElement and not products):
			print("No nutrition info available to be shown")
			pass
		
		portion = None if(not portionElement) else portionElement.text
		unit = None if(not unitElement) else unitElement.text

		nutritionInfo = []
		for prod in range(0, len(products), 3):
			nutritionInfo.append({products[prod].text: products[prod+1].text, "unit": products[prod+2].text })	
		
		dataset = {
			"prod_name":x["prod_name"] ,
			"prod_brand":x["prod_brand"] ,
			"prod_price":x["prod_price"] ,
			"prod_qty":x["prod_qty"] ,
			"prod_seller": "continente",
			"prod_nutri_info":[portion, unit, nutritionInfo]
		}
		
		print("\t",dataset, "\n")	
		f.write(json.dumps(dataset, ensure_ascii=False) + ",\n")		
	
