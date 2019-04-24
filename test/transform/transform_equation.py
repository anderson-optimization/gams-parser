from gams_parser import GamsParser

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("TEst")


def test_transform_equation_def():
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
