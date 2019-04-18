from lark import Lark, Transformer

with open('./grammar/ao_inject.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)

def test_ao_inject():
	with open('./test/gams/misc-comments.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())
