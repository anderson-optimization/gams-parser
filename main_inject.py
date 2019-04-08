from lark import Lark, Transformer

with open('ao_inject.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)



class TreeToModel(Transformer):
	def start(self,args):
		print("Start",args)
		return "".join(args)

	def statement(self,args):
		print('Statement',args)
		return "".join(args)

	def white_space(self,args):
		print("White space",args)
		return args[0].value

	def newline(self,args):
		return args[0].value

	def ao_macro(self,args):
		print("Ao Macro",args)
		return "<-- AO {} -->".format(args[1].value) + "".join(args[2:])


with open('./test/example-ao-inject.gms','r') as in_file:
	text=in_file.read()
	print(text)

	parse_tree=l.parse(text)
	gams_file=TreeToModel().transform(parse_tree)
	print(parse_tree)
	print(parse_tree.pretty())
	print(gams_file)