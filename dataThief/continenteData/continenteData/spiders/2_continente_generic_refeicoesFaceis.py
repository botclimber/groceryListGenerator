import scrapy

class ContinentDataExtractor(scrapy.Spider):

	name = "continenteData_refeicoesFaceis"
	start_urls = ["https://www.continente.pt/refeicoes-faceis/?start=0&srule=Fresh%20-RF&pmin=0.01"]
	custom_settings = {
		'ROBOTSTXT_OBEY': False,
	}

	totalProducts = 587
	bunchOfCurrentProducts = 0
		
	def parse(self, response):
		productsProcessed = self.bunchOfCurrentProducts + 24
		print( productsProcessed, " products handled! \n")

		products = response.xpath("//div[@class='ct-inner-tile-wrap col-inner-tile-wrap row no-gutters justify-content-center align-content-start']")
		
		prod_names = products.xpath("//a[@class='pwc-tile--description col-tile--description']/text()").getall()[-24:]
		prod_details = products.xpath("//a[@class='pwc-tile--description col-tile--description']/@href").getall()[-24:]
		prod_brands = products.xpath("//p[@class='pwc-tile--brand col-tile--brand']/text()").getall()[-24:]
		prod_prices = products.xpath("//span[@class='ct-price-formatted']/text()").getall()[-24:]
		prod_qtys = products.xpath("//p[@class='pwc-tile--quantity col-tile--quantity']/text()").getall()[-24:]
	
		yield {"bunchOf24Products": {"prod_names": prod_names, "prod_details_link": prod_details, "prod_brands": prod_brands, "prod_prices": prod_prices, "prod_qtys": prod_qtys}}
		
		# go to next page
		self.totalProducts -= 24
		if(self.totalProducts <= 0):
			print("All Products Extracted!")
			return

		else:
			self.bunchOfCurrentProducts += 24
			next_page = f"https://www.continente.pt/refeicoes-faceis/?start={self.bunchOfCurrentProducts}&srule=Fresh%20-RF&pmin=0.01"
			print(next_page)
			yield response.follow(next_page, callback=self.parse)
