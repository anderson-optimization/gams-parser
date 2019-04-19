from gams_parser import GamsParser

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("TEst")

def test_transform_multi_sets():
	with open('./test/gams/set-multi.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		model=gp.transform()

		print("\nModel\n")
		print(model)

		print("\nSets:\n")
		for s in model.set():
			print(s)

def test_transform_tuple_set():
	with open('./test/gams/set-tuple.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

		model=gp.transform()
		print("\nModel\n")
		print(model)

		print("\nSets:\n")
		for s in model.set():
			print(s)
