from lark import Lark, Transformer

with open('./grammer/gams.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)

def test_table_basic():
	with open('./test/gams/table-basic.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())
