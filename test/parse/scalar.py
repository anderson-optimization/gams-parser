from gams_parser import GamsParser

def test_scalar_basic():
	with open('./test/gams/scalar-basic.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())
