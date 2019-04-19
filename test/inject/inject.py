from gams_parser import GamsParser

def test_ao_inject():
	with open('./test/gams/misc-comments.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())
