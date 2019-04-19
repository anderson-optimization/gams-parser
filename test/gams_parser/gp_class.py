
from gams_parser import GamsParser

def test_open_file():
	gp = GamsParser('./test/gams/set-ranged.gms')
	parse_tree=gp.parse()
	print(parse_tree.pretty())
