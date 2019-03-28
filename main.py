from lark import Lark

with open('grammer.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)


with open('example-set-include.gms','r') as in_file:
	text=in_file.read()
	print(text)

	parsed=l.parse(text)
	print(parsed)
	print(parsed.pretty())
#print( l.parse("Hello, World!") )