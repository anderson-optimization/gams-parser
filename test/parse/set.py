from gams_parser import GamsParser

def test_set_basic():
	with open('./test/gams/set-basic.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_set_alias():
	with open('./test/gams/set-alias.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_set_indexed():
	with open('./test/gams/set-indexed.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())


def test_set_ranged():
	with open('./test/gams/set-ranged.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())


def test_set_multi():
	with open('./test/gams/set-multi.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_set_include():
	with open('./test/gams/set-include.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_set_tuple():
	with open('./test/gams/set-tuple.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())