from gams_parser import GamsParser

def test_parameter_basic():
	with open('./test/gams/parameter-basic.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_parameter_tuple():
	with open('./test/gams/parameter-tuple.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())
