from lark import Lark, Transformer

with open('./grammer/gams.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)

def test_real_shopmodel():
	with open('./test/gams/real-shopmodel.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())


def test_real_eminit():
	with open('./test/gams/real-eminit.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())


def test_real_siteanalysis():
	with open('./test/gams/real-siteanalysis.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())
