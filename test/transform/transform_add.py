from gams_parser import GamsParser

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("TEst")

def test_transform_real_shopmodel():
	with 	open('./test/gams/inject-datagen.inc','r') as gen_file, \
			open('./test/gams/inject-datademand.inc','r') as demand_file, \
			open('./test/gams/inject-siteanalysis.gms','r') as main_file:
		
		gp_main = GamsParser(main_file)	
		gp_gen = GamsParser(gen_file)
		gp_demand = GamsParser(demand_file)

		model_main = gp_main.transform()
		model_gen = gp_gen.transform()
		model_demand = gp_gen.transform()

		model = model_main + model_gen + model_demand


		print("\nModel\n")
		print(model)

		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)