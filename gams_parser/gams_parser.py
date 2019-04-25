
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

def scrub(obj, bad=["_meta","meta"]):
    if isinstance(obj, dict):
        for k in obj.keys():
            if k in bad:
                del obj[k]
            else:
                scrub(obj[k], bad)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] in bad:
                del obj[i]
            else:
                scrub(obj[i], bad)

    else:
        # neither a dict nor a list, do nothing
        pass


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

	def symbol_name(self,children,meta):
		if len(children)>1:
			raise Exception("Only a single identifier allowed for name")
		logger.debug('Create symbol name={}'.format(children[0]))
		return SymbolName('symbol_name',children,meta=meta)


	def definition(self,children,meta):
		return Definition(children,meta)

	def model_definition(self,children,meta):
		return ModelDefinition('model_definition',children,meta)

	def solve_definition(self,children,meta):
		return SolveDefinition('solve_definition',children,meta)

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


	def start(self,children,meta):
		model = Model()
		logger.debug("Process Statements")
		for statement in children:
			try:
				logger.debug("Processing new statement.")	
				if isinstance(statement,Tree) and statement.data=='equation_definition':
					logger.debug('Have equation defintion')
					model.add_equation(statement)
				elif isinstance(statement,Tree) and statement.data=='model_definition':
					logger.debug('Have model definition')
					model.add_model(statement)
				elif isinstance(statement,Tree) and statement.data=='solve_definition':
					logger.debug('Have solve statement')
					model.add_solve(statement)
				elif isinstance(statement,list):
					logger.debug('Have symbol list')
					for symbol_def in statement:
						model.add_symbol(symbol_def)
				else:
					logger.debug('Unknown statement')
					print("Statement",statement.data)
					raise Exception("Statement type not handled")
				logger.debug("Finished statement.")
			except Exception as e:
				logger.error("Statement not processed, error: {}".format(e))
				print(statement)
		return model


class Description():
	pass


class EquationDefinition():
	pass

class ModelDefinition(Tree):
	def __init__(self,data,children,meta=None):
		self.name=children[0]
		self.equations=children[1:]
		Tree.__init__(self,data,children,meta=meta)

	def __repr__(self):
		return "<model={} eqn={}>".format(self.name,",".join([str(e) for e in self.equations]))

class SolveDefinition(Tree):
	def __init__(self,data,children,meta=None):
		print("Solve Model",children)
		self.name=children[0]
		for c in children:
			if isinstance(c,Tree) and c.data == 'sense_min':
				self.sense='min'
			elif isinstance(c,Tree) and c.data == 'sense_max':
				self.sense='max'
			elif isinstance(c,SymbolName):
				self.obj=c
			else:
				 print("Dont recognize")
		Tree.__init__(self,data,children,meta=meta)

	def __repr__(self):
		return "-> solve model={name} {sense} {obj}".format(name=self.name,sense=self.sense,obj=self.obj)


class SymbolName(Tree):
	def __init__(self,data,children,meta=None):
		self.name=children[0]
		Tree.__init__(self,data,children,meta=meta)

	def __str__(self):
		return self.name

	def __repr__(self):
		return "__{name}__".format(name=self.name)

class IndexList(Tree):
	def items(self):
		return [s.name for s in self.children]

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
		self.assignments=[]
		self.model_defs=[]
		self.model_solve=[]

	def add_equation(self,e):
		print('Model : Add equation',e)
		eqn_def=EquationDefinition()
		eqn_def.symbol=Symbol(e.children[0])
		eqn_def.meta=e.meta
		eqn_def.symbol_ref=[]
		for s in e.find_data('symbol_name'):
			logger.debug('Found symbol ref: {}'.format(s))
			eqn_def.symbol_ref.append(s)
		self.equation_defs.append(eqn_def)

	def add_model(self,m):
		self.model_defs.append(m)

	def add_solve(self,s):
		self.model_solve.append(s)

	def add_symbol(self,e):
		if not e.symbol_type:
			raise Exception('Symbol does not have a type!')
		elif e.symbol_type not in self.symbols:
			raise Exception('Symbol type not found')
		self.symbols[e.symbol_type].append(e)
		logger.info("Symbol[{type}]={name} added to model".format(name=e.symbol.name,type=e.symbol_type))

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
					i.symbol_ref=j.symbol_ref
					print("Refs",i.symbol_ref)

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
			s.text="".join(text)


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

		for m in self.model_defs:
			output.append("\n{}".format(m))

		for s in self.model_solve:
			output.append("\n{}".format(s))

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
		self.name=info[0].name
		logger.debug("Creating Symbol: {}".format(self.name))
		if len(info)>1:
			self.index_list=info[1].items()

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
