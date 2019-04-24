
from lark import Lark, Transformer, Tree, Token
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

class TreeToModel(Transformer):    
	def string(self, args):
		return "".join(args)

	def value(self,args):
		return float(args[0])

	# def symbol_element(self,args):
	# 	return SymbolId("".join(args))

	def symbol_name(self,args):
		if len(args)>1:
			print("args",args)
			raise Exception("Only a single identifier allowed for name")
		return args[0]


	# def description(self,args):
	# 	return Description(args[0].strip("'"))

	def definition(self,args):
		return Definition(args)

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

	def index_list(self,args):
		logger.debug("IndexList {}".format(args))
		return args

	def set_list(self,args):		
		for set_def in args:
			set_def.symbol_type='set'
		return args

	def parameter_list(self,args):
		for set_def in args:
			set_def.symbol_type='parameter'
		return args

	def variable_list(self,args):
		for set_def in args:
			set_def.symbol_type='variable'
		return args

	def scalar_list(self,args):
		for set_def in args:
			set_def.symbol_type='scalar'
		return args

	def equation_list(self,args):
		print('equation list args',args)
		for set_def in args:
			set_def.symbol_type='equation'
		return args

	def table_list(self,args):
		for set_def in args:
			set_def.symbol_type='table'
		return args

	def variable_list(self,args):
		for set_def in args:
			set_def.symbol_type='variable'
		return args


	def start(self,args):
		model = Model()
		print("Process Statements")
		#print('Statements',args)
		for statement in args:
			try:			
				if isinstance(statement,Tree) and statement.data=='equation_definition':
					model.add_equation(statement)
				else:
					for symbol_def in statement:
						model.add_symbol(symbol_def)
			except Exception as e:
				logger.error("Statement not processed, error: {}".format(e))
		return model


class Description():
	pass


class EquationDefinition():
	pass

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
		print('Model : Add equation',e.__dict__)
		eqn_def=EquationDefinition()
		eqn_def.symbol=Symbol(e.children[0])
		eqn_def.meta=e.meta
		self.equation_defs.append(eqn_def)

	def add_symbol(self,e):
		print("Model : Add symbol",e)
		if not e.symbol_type:
			raise Exception('Symbol does not have a type!')
		elif e.symbol_type not in self.symbols:
			raise Exception('Symbol type not found')
		self.symbols[e.symbol_type].append(e)

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
				text.append("\n\nEquation Definition:\n")
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

	def __init__(self,args,meta=None):
		logger.debug("Build Definition: {}".format(args))
		print('definition',args)
		self._meta=meta
		for a in args:
			if isinstance(a,Tree) and a.data=='symbol':
				print("Symbol",a)
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
		print('symbol new',tree)
		info=tree.children
		self.symbol_name=info[0]
		logger.debug("Creating Symbol: {}".format(self.symbol_name))
		if len(info)>1:
			self.index_list=info[1]

	def __eq__(self,other):
		return self.symbol_name == other.symbol_name

	def __repr__(self):
		if self.index_list: 
			return '__{symbol_name}({index_list})__'.format(symbol_name=self.symbol_name,index_list=",".join(self.index_list))
		else:
			return '__{symbol_name}__'.format(symbol_name=self.symbol_name)


class SymbolId():
	def __init__(self,sid):
		logger.debug("Creating Symbol ID {}".format(sid))
		self.sid=str(sid)

	def __str__(self):
		return self.sid

	def __repr__(self):
		return '*{sid}*'.format(sid=self.sid)


# class Expression():
# 	pass




# class TreeToModel(Transformer):
# 	def start(self,args):
# 		logger.debug('Start',args)
# 		model=Model()
# 		for line in args:
# 			try:
# 				for item in line:
# 					model.add(item)
					
# 			except Exception as e:
# 				logger.debug('exception ',e)
# 		logger.debug('Model',model)
# 		return model

# 	def id(self,args):
# 		#logger.debug("ID Word",args)
# 		return str(args[0].value)

# 	def dimension_id(self,args):
# 		logger.debug("dimension id",args)
# 		return args

# 	def group_definition(self,args):
# 		command=args[0]
# 		logger.debug("Group Definition",args)
# 		items=[]
# 		for define in args[1:-2]:
# 			if command.data=='set':
# 				items.append(Set(define))
# 			elif command.data=='parameter':
# 				items.append(Parameter(define))
# 		return items


# 	def comment(self,args):
# 		logger.debug("Comment",args)
# 		return args

# 	def ao_macro(self,args):
# 		logger.debug("AO",args)
# 		return args

# with open('./test/site-analysis.gms','r') as in_file:
# 	text=in_file.read()
# 	#logger.debug(text)

# 	parse_tree=l.parse(text)
# 	logger.debug(parse_tree)
# 	logger.debug(parse_tree.pretty())
# 	for inst in parse_tree.children:
# 		line_type=inst.data
# 		if line_type=='group_definition':
# 			symbol_type=inst.children[0].data
# 			logger.debug(line_type,symbol_type)
# 			for define in inst.children[1:]:
# 				try:
# 					logger.debug(define.pretty())
# 				except:
# 					pass

# 	model=TreeToModel().transform(parse_tree)

# 	for s in model.sets:
# 		logger.debug(s)

# 	for p in model.parameters:
# 		logger.debug(p)