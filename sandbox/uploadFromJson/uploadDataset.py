import json
import numpy as np

class ReadDataset:

	def __init__(self, file):

		self.f = open(file, "r", encoding='utf-8')
		self.data = json.load(self.f)
		self.f.close()    

	def getData(self):
		return self.data

x = ReadDataset("../../data/continente_dataset_detailed_2023129.json")
refeicoes_rapidas = x.getData()["refeicoes_rapidas"]

for d in refeicoes_rapidas:
    print(d)