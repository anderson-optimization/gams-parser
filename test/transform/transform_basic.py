from gams_parser import GamsParser

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("TEst")

def test_transform_multi_sets():
	with open('./test/gams/set-multi.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)

		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)

def test_transform_tuple_set():
	with open('./test/gams/set-tuple.gms','r') as in_file:
		gp = GamsParser(in_file)		
		model=gp.transform()

		print("\nModel\n")
		print(model)
		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)


def test_transform_indexed_set():
	with open('./test/gams/set-indexed.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)
		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)



def test_transform_parameter():
	with open('./test/gams/parameter-tuple.gms','r') as in_file:
		gp = GamsParser(in_file)
		model=gp.transform()

		print("\nModel\n")
		print(model)
		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)

def test_transform_variable():
	with open('./test/gams/variable-basic.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())
		model=gp.transform()

		print("\nModel\n")
		print(model)
		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)


def test_transform_equation():
	with open('./test/gams/equation-basic.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())
		model=gp.transform()

		print("\nModel\n")
		print(model)
		print("\nSymbols:\n")
		for s in model.symbol():
			print(s)
