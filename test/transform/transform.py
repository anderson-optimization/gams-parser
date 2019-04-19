from gams_parser import GamsParser

def test_transform():
	with open('./test/gams/set-multi.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		transformed=gp.transform()

		print(parse_tree.pretty())
