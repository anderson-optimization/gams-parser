from gams_parser import GamsParser

def test_equation_basic():
	with open('./test/gams/equation-basic.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_equation_indexoperator():
	with open('./test/gams/equation-indexoperator.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_equation_elementindex():
	with open('./test/gams/equation-elementindex.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())
