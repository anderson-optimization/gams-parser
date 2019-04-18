from lark import Lark, Transformer

with open('./grammar/gams.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text,propagate_positions=True)

def test_set_basic():
	with open('./test/gams/set-basic.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

def test_set_alias():
	with open('./test/gams/set-alias.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

def test_set_indexed():
	with open('./test/gams/set-indexed.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())


def test_set_ranged():
	with open('./test/gams/set-ranged.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())


def test_set_multi():
	with open('./test/gams/set-multi.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

def test_set_include():
	with open('./test/gams/set-include.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())

def test_set_tuple():
	with open('./test/gams/set-tuple.gms','r') as in_file:
		text=in_file.read()
		parse_tree=l.parse(text)
		print(parse_tree.pretty())