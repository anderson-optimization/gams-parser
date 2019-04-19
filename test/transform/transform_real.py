from gams_parser import GamsParser

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("TEst")

def test_transform_real_shopmodel():
	with open('./test/gams/real-shopmodel.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)

		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)


def test_transform_real_eminit():
	with open('./test/gams/real-eminit.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)

		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)



def test_transform_real_siteanalysis():
	with open('./test/gams/real-siteanalysis.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)

		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)
