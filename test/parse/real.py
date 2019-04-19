from gams_parser import GamsParser

def test_real_shopmodel():
	with open('./test/gams/real-shopmodel.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())


def test_real_eminit():
	with open('./test/gams/real-eminit.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())


def test_real_siteanalysis():
	with open('./test/gams/real-siteanalysis.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())
