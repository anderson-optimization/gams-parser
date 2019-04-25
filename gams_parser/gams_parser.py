
from lark import Lark, Transformer, Tree, Token, v_args
from lark.tree import Meta
import os
import json

import logging
logger = logging.getLogger('gams_parser')


dirname = os.path.dirname(__file__)
grammar_gams = os.path.join(dirname, 'grammar_gams.lark')
grammar_ao_inject = os.path.join(dirname, 'grammar_ao_inject.lark')


with open(grammar_gams,'r') as in_file:
	text=in_file.read()
	lark_gams = Lark(text,propagate_positions=True)

with open(grammar_ao_inject,'r') as in_file:
	text=in_file.read()
	lark_ao_inject = Lark(text)



class GamsParser():
	def __init__(self,file):
		if isinstance(file,str):
			self.file = open(file,'r')
		else:
			self.file = file

		self.text=self.file.read()

	def parse(self):
		return lark_gams.parse(self.text)

	def transform(self):
		parse_tree=lark_gams.parse(self.text)
		model=TreeToModel().transform(parse_tree)
		model.cross_reference()
		model.reference_lines(self.text)
		return model

@v_args(meta=True)
class TreeToModel(Transformer):    
	def string(self,args,meta):
		return "".join(args)

	def value(self,args,meta):
		return float(args[0])

	# def symbol_element(self,args):
	# 	return SymbolId("".join(args))

	def symbol_name(self,children,meta):
		print('Create symbol name',children)
		if len(children)>1:
			raise Exception("Only a single identifier allowed for name")
		return SymbolName('symbol_name',children,meta=meta)


	# def description(self,args):
	# 	return Description(args[0].strip("'"))

	def definition(self,children,meta):
		print("Creating Definition")
		return Definition(children,meta)

	# def equation_definition(self,args):
	# 	#print(args.data)
	# 	for a in args:
	# 		print(a)
	# 		print(a.__dict__)
	# 	return args

	# def symbol(self,args):
	# 	logger.debug('Symbol {}'.format(args))
	# 	symb=Symbol(args)
	# 	return symb

	# def symbol_id(self,args):
	# 	logger.debug("SymbolID {}".format(args))

	# 	return SymbolId(".".join([str(a) for a in args]))

	def index_list(self,chilren,meta):
		logger.debug("IndexList {}".format(chilren))
		return IndexList('index_list',chilren,meta)

	def set_list(self,args,meta):		
		for set_def in args:
			set_def.symbol_type='set'
		return args

	def parameter_list(self,args,meta):
		for set_def in args:
			set_def.symbol_type='parameter'
		return args

	def variable_list(self,args,meta):
		for set_def in args:
			set_def.symbol_type='variable'
		return args

	def scalar_list(self,args,meta):
		for set_def in args:
			set_def.symbol_type='scalar'
		return args

	def equation_list(self,args,meta):
		#print('equation list args',args)
		for set_def in args:
			set_def.symbol_type='equation'
		return args

	def table_list(self,args,meta):
		for set_def in args:
			set_def.symbol_type='table'
		return args

	def variable_list(self,args,meta):
		for set_def in args:
			set_def.symbol_type='variable'
		return args


	def start(self,args,meta):
		model = Model()
		print("Process Statements")
		#print('Statements',args)
		for statement in args:
			try:
				print("Processing new statement.")	
				if isinstance(statement,Tree) and statement.data=='equation_definition':
					model.add_equation(statement)
				else:
					for symbol_def in statement:
						model.add_symbol(symbol_def)
				print("Finished statement.")
			except Exception as e:
				logger.error("Statement not processed, error: {}".format(e))
		return model


class Description():
	pass


class EquationDefinition():
	pass

class SymbolName(Tree):
	def name(self):
		return "".join(self.children)

	def __str__(self):
		return self.name()

	def __repr__(self):
		return "__{name}__".format(name=self.name())

class IndexList(Tree):
	def __repr__(self):
		return "({items})".format(items=",".join([str(c) for c in self.children]))

class Model(object):
	symbols={}

	def __init__(self):
		self.symbols={
			"set": [],
			"parameter": [],
			"variable": [],
			"equation": [],
			"scalar": [],
			"table": []
		}
		self.equation_defs=[]

	def add_equation(self,e):
		print('Model : Add equation',e)
		eqn_def=EquationDefinition()
		eqn_def.symbol=Symbol(e.children[0])
		eqn_def.meta=e.meta
		for s in e.find_data('symbol_name'):
			print('Found symbol refs',s)
		self.equation_defs.append(eqn_def)

	def add_symbol(self,e):
		print("Model : Adding symbol")
		if not e.symbol_type:
			raise Exception('Symbol does not have a type!')
		elif e.symbol_type not in self.symbols:
			raise Exception('Symbol type not found')
		self.symbols[e.symbol_type].append(e)
		print("Symbol Added!")

	def set(self):
		return self.symbols['set']

	def parameter(self):
		return self.symbols['parameter']

	def equation(self):
		return self.symbols['equation']

	def variable(self):
		return self.symbols['variable']

	def scalar(self):
		return self.symbols['scalar']

	def symbol(self):
		for i in self.symbols:
			for j in self.symbols[i]:
				yield j

	def cross_reference(self):
		print("CrossREFERENCE")
		for i in self.symbols['equation']:
			for j in self.equation_defs:
				if i.symbol==j.symbol:
					print('I',i)
					print('J',j)
					i.equation=j

	def reference_lines(self,text):
		lines=text.splitlines()
		for s in self.symbol():
			print("Reference line for symbol {}".format(s))
			line=s.meta.line-1
			end_line=s.meta.end_line
			text=["\n".join(lines[line:end_line])]
			if s.equation:
				text.insert(0,"*** Symbol Definition ***\n\n")
				text.append("\n\n*** Equation Definition ***\n\n")
				line=s.equation.meta.line-1
				end_line=s.equation.meta.end_line
				text.append("\n".join(lines[line:end_line]))
			s.meta.text="".join(text)

		#for s in 


	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def toDict(self):
		return json.loads(self.toJSON())


	def __repr__(self):
		output=["model:"]

		for i in self.symbols:
			if len(self.symbols[i])>0:
				output.append("n_{name}={num}".format(name=i,num=len(self.symbols[i])))

		return " ".join(output)


class Data():
	def __init__(self,args):
		logger.debug("BUILD Data {}".format(args))
		self.data=args

	def __repr__(self):
		return "<data block len={length}>".format(length=len(self.data))

class Definition():
	symbol_type=None
	symbol=None
	description=None
	data=None
	equation=None
	symbol_ref=[]

	def __init__(self,args,meta):
		#logger.debug("Build Definition: {}".format(args))
		#print('definition',args)
		self._meta=meta
		for a in args:
			print("Definition data: ",a.data)
			if isinstance(a,Tree) and a.data=='symbol':
				#print("Symbol",a)
				self.symbol=Symbol(a)
				self.meta.line=a.meta.line
				self.meta.end_line=a.meta.end_line
				self.meta.empty=False
			elif isinstance(a,Tree) and a.data=="description":
				print(a)
				print(a.data)
				self.description="".join(a.children).strip("'")
				self.meta.end_line=a.end_line
			elif isinstance(a,Tree) and a.data=="data":
				self.data=a
				self.meta.end_line=a.end_line

	@property
	def meta(self):
		if self._meta is None:
			self._meta = Meta()
		return self._meta

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def __repr__(self):
		output=[]
		if self.symbol_type:
			output.append('[{}]'.format(self.symbol_type))
		output.append('{}'.format(self.symbol))
		if self.description:
			output.append('"{}"'.format(self.description))
		if self.data:
			output.append('{}'.format(self.data))
		return " ".join(output)


## This should have index list
class Symbol():
	symbol_name=None
	index_list=None

	def __init__(self,tree):
		if tree.data != 'symbol':
			raise Exception("Not a symbol def")
		print('symbol new')
		info=tree.children
		self.symbol_name=info[0]
		self.name="".join(self.symbol_name.children)
		logger.debug("Creating Symbol: {}".format(self.symbol_name))
		if len(info)>1:
			self.index_list=info[1]

	def __eq__(self,other):
		return self.name == other.name

	def __repr__(self):
		if self.index_list: 
			return '__{symbol_name}{index_list}__'.format(symbol_name=self.name,index_list=self.index_list)
		else:
			return '__{symbol_name}__'.format(symbol_name=self.name)


class SymbolId():
	def __init__(self,sid):
		logger.debug("Creating Symbol ID {}".format(sid))
		self.sid=str(sid)

	def __str__(self):
		return self.sid

	def __repr__(self):
		return '*{sid}*'.format(sid=self.sid)
