import json
import numpy as np

class ReadFromJSON:
	
	FILE = "continenteProductsData.json"

	def __init__(self):
		self.f = open(self.FILE)
		self.data = json.load(self.f)
		self.transformedData = self.__transformData()
		self.f.close()		

	def __transformData(self):
		aggrProductsDict = []

		aggrProducts = []
		for x in self.data["List"]:
			products = x["bunchOf24Products"]
			zipped = np.array(list(zip(products["prod_names"], products["prod_details_link"], products["prod_brands"], products["prod_prices"], products["prod_qtys"])))
			
			for h in zipped:
				aggrProducts.append(h)

		for y in aggrProducts:
			
			prod_name = y[0]	
			prod_link = y[1]
			prod_brand = y[2]
			prod_price = y[3].replace("\n", "").replace(",", ".").replace("€","")		
			prod_qty = y[4]			

			aggrProductsDict.append({"prod_name": prod_name, "prod_link": prod_link, "prod_brand": prod_brand, "prod_price": prod_price, "prod_qty": prod_qty})	
	
		rmDuplicates = list({ dictionary['prod_name']: dictionary for dictionary in aggrProductsDict}.values())
		
		print("raw data size: ", len(aggrProductsDict))
		print("Cleaned data size: ", len(rmDuplicates))

		return rmDuplicates 

	def getData(self):
		return self.transformedData


x = ReadFromJSON().getData()

print(x[0]["prod_link"])
