from gams_parser import GamsParser

def test_assignment_basic():
	with open('./test/gams/assignment-basic.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_assignment_expansion():
	with open('./test/gams/assignment-expansion.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())


def test_assignment_conditional():
	with open('./test/gams/assignment-conditional.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())


def test_assignment_suffix():
	with open('./test/gams/assignment-suffix.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

