from lark import Lark, Transformer

with open('./grammar/gams.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)

def test_equation_basic():
	with open('./test/gams/equation-basic.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

def test_equation_indexoperator():
	with open('./test/gams/equation-indexoperator.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

def test_equation_elementindex():
	with open('./test/gams/equation-elementindex.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())
