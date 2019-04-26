from gams_parser import GamsParser, scrub
import json 
import pprint
import logging
logging.basicConfig(level=logging.DEBUG)

def test_transform_def_dict():
	with open('./test/gams/real-shopmodel.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)

		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)
			#print(s.toJSON())



def test_transform_model_json():
	with open('./test/gams/real-shopmodel2.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)

		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)

		dm=model.toJSON()

		#print("\nmodel.toJSON\n")
		#print(dm)

		print("\nmodel.toDict Hack\n")
		m=model.toDict()
		scrub(m)
		pprint.pprint(m['assignments'])

def test_transform_model_siteanalysis():
	with open('./test/gams/real-siteanalysis.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)

		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)

		dm=model.toJSON()

		#print("\nmodel.toJSON\n")
		#print(dm)

		print("\nmodel.toDict Hack\n")
		m=model.toDict()
		scrub(m)
		pprint.pprint(m)
