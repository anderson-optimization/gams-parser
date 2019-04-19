from gams_parser import GamsParser

def test_variable_basic():
	with open('./test/gams/variable-basic.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())