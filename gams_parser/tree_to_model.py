
from lark import Transformer, Tree, Token, v_args
from lark.tree import Meta

import json

import logging
logger = logging.getLogger('gams_parser.model')

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

	def assignment_definition(self,children,meta):
		return AssignmentDefinition('assignment_definition',children,meta)

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
				elif isinstance(statement,Tree) and statement.data=='assignment_definition':
					logger.debug('Have assignment statement')
					model.add_assignment(statement)
				elif isinstance(statement,list):
					logger.debug('Have symbol list')
					for symbol_def in statement:
						model.add_symbol(symbol_def)
				else:
					logger.debug('Unknown statement')
					logger.debug("Statement data",statement.data)
					raise Exception("Statement type not handled")
				logger.debug("Finished statement.")
			except Exception as e:
				logger.error("Statement not processed, error: {}".format(e))
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
		self.name=children[0]
		for c in children:
			if isinstance(c,Tree) and c.data == 'sense_min':
				self.sense='min'
			elif isinstance(c,Tree) and c.data == 'sense_max':
				self.sense='max'
			elif isinstance(c,SymbolName):
				self.obj=c
			else:
				 logger.warning("Solve definition, dont recognize child")
		Tree.__init__(self,data,children,meta=meta)

	def __repr__(self):
		return "-> solve model={name} {sense} {obj}".format(name=self.name,sense=self.sense,obj=self.obj)

class AssignmentDefinition(Tree):
	def __init__(self,data,children,meta=None):
		self.symbol_refs=[]
		refs=set()
		for s in children:
			if isinstance(s,SymbolName):
				refs.add(s.name)
			elif isinstance(s,Tree):
				for s in s.find_data('symbol_name'):
					refs.add(s.name)
		self.symbol_refs=list(refs)
		Tree.__init__(self,data,children,meta=meta)


	def __repr__(self):
		return "<assignment n_symbols={num}>".format(num=len(self.symbol_refs))



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
		self.solve=[]

	def __add__(self,other):
		model = Model()
		for s in self.symbols:
			model.symbols[s]=self.symbols[s]+other.symbols[s]
		model.equation_defs=self.equation_defs+other.equation_defs
		model.assignments=self.assignments+other.assignments
		model.model_defs=self.model_defs+other.model_defs
		model.solve=self.solve+other.solve
		return model

	def add_equation(self,e):
		eqn_def=EquationDefinition()
		eqn_def.symbol=Symbol(e.children[0])
		eqn_def.meta=e.meta
		eqn_def.symbol_ref=[]
		for s in e.find_data('symbol_name'):
			logger.debug('Found symbol ref: {}'.format(s))
			eqn_def.symbol_ref.append(s)
		self.equation_defs.append(eqn_def)

	def add_assignment(self,a):
		self.assignments.append(a)

	def add_model(self,m):
		self.model_defs.append(m)

	def add_solve(self,s):
		self.solve.append(s)

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
		logger.debug("CrossREFERENCEing")
		for i in self.symbols['equation']:
			for j in self.equation_defs:
				if i.symbol==j.symbol:
					logger.debug('CR Match')
					i.equation=j
					i.symbol_ref=j.symbol_ref

	def reference_lines(self,text):
		lines=text.splitlines()
		for s in self.symbol():
			logger.debug("Reference line for symbol {}".format(s))
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
		for a in self.assignments:
			logger.debug("Reference line for assignment {}".format(a))
			line=a.meta.line-1
			end_line=a.meta.end_line
			text=["\n".join(lines[line:end_line])]
			a.text="".join(text)



	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)

	def toDict(self):
		return json.loads(self.toJSON())


	def __repr__(self):
		output=["** model **","\nsymbols:"]
		for i in self.symbols:
			if len(self.symbols[i])>0:
				output.append("n_{name}={num}".format(name=i,num=len(self.symbols[i])))
		if len(self.assignments)>0:
			output.append("\nn_assignments={num}".format(num=len(self.assignments)))


		for m in self.model_defs:
			output.append("\n{}".format(m))

		for s in self.solve:
			output.append("\n{}".format(s))

		output.append("\n** end model **")
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
		self._meta=meta
		for a in args:
			if isinstance(a,Tree) and a.data=='symbol':
				self.symbol=Symbol(a)
				self.meta.line=a.meta.line
				self.meta.end_line=a.meta.end_line
				self.meta.empty=False
			elif isinstance(a,Tree) and a.data=="description":
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
