from lark import Lark, Transformer

with open('./grammer/gams.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)

def test_assignment_basic():
	with open('./test/gams/assignment-basic.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

def test_assignment_expansion():
	with open('./test/gams/assignment-expansion.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())


def test_assignment_conditional():
	with open('./test/gams/assignment-conditional.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())


def test_assignment_suffix():
	with open('./test/gams/assignment-suffix.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

