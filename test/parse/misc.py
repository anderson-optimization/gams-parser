from gams_parser import GamsParser

def test_misc_comments():
	with open('./test/gams/misc-comments.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())

def test_misc_include():
	with open('./test/gams/misc-include.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())
 
def test_misc_conditional():
	with open('./test/gams/misc-conditional.gms','r') as in_file:
		gp = GamsParser(in_file)
		parse_tree=gp.parse()
		print(parse_tree.pretty())