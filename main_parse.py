from lark import Lark, Transformer

with open('gams_parse.lark','r') as in_file:
	text=in_file.read()
	l = Lark(text)


class Set():
	def __init__(self,definition):
		print("Creating Set",definition)
		self.definition=definition

	def __repr__(self):
		return 'set:{d}'.format(d=self.definition)

class Parameter():
	def __init__(self,definition):
		print("Creating Parameter",definition)
		self.definition=definition

	def __repr__(self):
		return 'param:{d}'.format(d=self.definition)

class Definition():
	def __init__(self,symbol=None,description=None):
		self.symbol=symbol
		self.description=description

	def __repr__(self):
		return '{symbol} {description}'.format(symbol=self.symbol,description=self.description)

class Symbol():
	def __init__(self,sid):
		print("Creating Symbol",sid)
		self.sid=str(sid)

	def __repr__(self):
		return '__{sid}__'.format(sid=self.sid)

class Description():
	def __init__(self,text):
		self.text=str(text.strip('"'))

	def __repr__(self):
		return '"' +self.text+'"'

class Expression():
	pass


class Model():
	sets=[]
	parameters=[]

	def add(self,e):
		if isinstance(e,Set):
			self.sets.append(e)
		elif isinstance(e,Parameter):
			self.parameters.append(e)
		else:
			print('Model : Uknown add',e)

	def __repr__(self):
		return "model: n_set={n_set} n_param={n_param}".format(n_set=len(self.sets),n_param=len(self.parameters))


class TreeToModel(Transformer):
	def start(self,args):
		print('Start',args)
		model=Model()
		for line in args:
			try:
				for item in line:
					model.add(item)
					
			except Exception as e:
				print('exception ',e)
		print('Model',model)
		return model

	def id(self,args):
		#print("ID Word",args)
		return str(args[0].value)

	def dimension_id(self,args):
		print("dimension id",args)
		return args

	def group_definition(self,args):
		command=args[0]
		print("Group Definition",args)
		items=[]
		for define in args[1:-2]:
			if command.data=='set':
				items.append(Set(define))
			elif command.data=='parameter':
				items.append(Parameter(define))
		return items

	def definition(self,args):
		print("Definition",args)
		return Definition(symbol=args[0],description=args[1])

	def symbol(self,args):
		print('Symbol',args)
		symb=Symbol(args[0])
		return symb

	def description(self,args):
		return Description(args[0].value)

	def comment(self,args):
		print("Comment",args)
		return args

	def ao_macro(self,args):
		print("AO",args)
		return args

with open('./test/example-ao-inject.gms','r') as in_file:
	text=in_file.read()
	#print(text)

	parse_tree=l.parse(text)
	print(parse_tree)
	print(parse_tree.pretty())
	for inst in parse_tree.children:
		line_type=inst.data
		if line_type=='group_definition':
			symbol_type=inst.children[0].data
			print(line_type,symbol_type)
			for define in inst.children[1:]:
				try:
					print(define.pretty())
				except:
					pass

	model=TreeToModel().transform(parse_tree)

	for s in model.sets:
		print(s)

	for p in model.parameters:
		print(p)