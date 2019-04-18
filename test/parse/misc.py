from lark import Lark, Transformer

with open('./grammar/gams.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)

def test_misc_comments():
	with open('./test/gams/misc-comments.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

def test_misc_include():
	with open('./test/gams/misc-include.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())
 
def test_misc_conditional():
	with open('./test/gams/misc-conditional.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())
