from lark import Lark, Transformer

with open('./grammar/gams.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)

def test_variable_basic():
	with open('./test/gams/variable-basic.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())
