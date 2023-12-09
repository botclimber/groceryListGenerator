from requests_html import HTMLSession
import json
import numpy as np
import datetime

from commonReader import ReadFromJSON

time_now = datetime.datetime.now()
currentDate = str(time_now.year)+str(time_now.month)+str(time_now.day)

category = "refeicoesFaceis"

instance = ReadFromJSON("../data/{inCategory}/continente_dataset_generic_{inCurrentDate}.json".format(inCategory = category, inCurrentDate = currentDate))
data = instance.getData()

s = HTMLSession()

with open("../data/{inCategory}/generated/continente_dataset_detailed_{inCurrentDate}.json".format(inCategory = category, inCurrentDate = currentDate), "a", encoding="utf-8") as f:
	for index, x in enumerate(data):
		print("Handling product ["+x["prod_name"]+"] with index ["+str(index)+"] ("+str(index+1)+" out of "+str(instance.transformedDataSize)+"):")
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
			nutritionInfo.append({products[prod].text: products[prod+1].text.replace(",","."), "unit": products[prod+2].text })	
		
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
	
