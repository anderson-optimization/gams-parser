
from lark import Transformer, Tree
from .util import get_path
import logging
import re
import json

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

logger = logging.getLogger('gams_parser.injector')
logger.setLevel('DEBUG')
def get_id(item):
	ao_item=None
	item_name=None
	item_id=None
	if isinstance(item,str):
		logger.debug('Getting id from string')
		item_name=item
		item_id=item
	elif item and 'id' in item:
		logger.debug('Getting id from item')
		ao_item = item
	elif item and 'item' in item and 'id' in item['item']:
		logger.debug('Getting id from nested item ref')
		ao_item=item['item']
	else:
		raise Exception("Unknown id format")

	if ao_item:
		item_id=ao_item['id']
		# Try to get name
		name=get_path(ao_item,'parameter.name.name')
		# Attempt project name
		if not name:
			name=get_path(ao_item,'step.start.parameter.name.name')

		if name:
			item_name=name
		else:
			item_name=item_id

	item_name=item_name.replace(" ",'').replace("-","_")
	# Hopefully this removes everything but a-zA-Z_
	item_name = re.sub(
			r"[^\w]",
			"",
			item_name
		)

#	print("item_name",item_id,item_name)

	return item_id,item_name

class TreeInjector(Transformer):
	def __init__(self,context,data=None):
		self._context=context
		self._data=data
		self._map=[]
		self._mapped=set()

	def _add_to_map(self,item_id=None,item_name=None,item=None):
		if not item_id:
			raise Exception("Need item id")
		if not item_name:
			raise Exception("Need item name")
		
		if item_id not in self._mapped:
			self._map.append({
					"item_id": item_id,
					"item_name": item_name,
					"item": item
				})
			self._mapped.add(item_id)

	def start(self,args):
		logger.debug("Start")
		return "".join(args),self._map

	def statement(self,args):
		#logger.debug('Statement')
		return "".join(args)

	def white_space(self,args):
		logger.debug("White space")
		return args[0].value

	def newline(self,args):
		return args[0].value

	def filter(self,args):
		logger.debug("Filter")
		def filter_fn(item):
			if args[1].data=='op_eq':
				return item[args[0]]==args[2]
			elif args[1].data=='op_sw':
				return item[args[0]].startswith(args[2])
			else:
				raise Exception("Unknown operator")
		return filter_fn

	def project(self,args):
		logger.debug("Project")
		items=[self._context['project']]
		return items

	def data(self,args):
		logger.debug("Data")
		items=self._context['data']
		return items

	def asset(self,args):
		logger.debug("Asset")
		items=self._context['asset']
		if len(args)>0:
			items=[i for i in items if args[0](i)]
		return items
		
	def item_exp(self,args):
		logger.debug("Item Expr")
		items=args[0]
		
		# If Children, filter
		if len(args)>1:
			filter_fn=args[1]
			items=[i for i in items if filter_fn(i)]

		return items

	def cmd_jsondata(self,args):
		logger.debug("cmd JsonData")

		data_selector=args[0]

		out_items=[]
		data_item=None
		data_by_col=None
		if data_selector.data=='data_by_key':
			key="".join(data_selector.children)
			data = self._data[key]
		elif data_selector.data=='data_by_group':
			group="".join(data_selector.children)
			data_items=[d for d in self._context['data'] if d['groupKey']==group]
			if len(data_items)>1:
				raise Exception("Only support single data selectors for now")
			data_item=data_items[0]
			data_id,data_name=get_id(data_item)
			data=self._data[data_id]
			out_items.append('\t{}'.format(data_name))
		else:
			raise Exception("Data selector not supported")


		columns=[]
		for a in args[1:]:
			for c in a.children:
				columns.append(c)

		for r in range(len(data)):
			row_template="".join(columns)
			row_data=AttrDict(data[r])
			if data_item:
				data_by_col = [data[r][c['prop']] for c in data_item['item']['columns']]
			row_str=row_template.format(_index=r,_index_p1=r+1,row=row_data,col=data_by_col)
			out_items.append(row_str)

		return "\n".join(out_items)


	def cmd_param(self,args):
		logger.debug("cmd Param")
		items=args[0]
		## ASSUME SELECTORS
		selector=args[1]
		if len(selector.children)>1:
			raise Exception("Only one selector allowed")
		selector=selector.children[0].strip("'")

		out_items=[]
		for item in items:
			item_id,item_name=get_id(item)
			self._add_to_map(item_id=item_id,item_name=item_name,item=item)
			logger.debug("Item")
			logger.debug("Selector {}".format(selector))
			if 'item' in item:
				value=get_path(item['item'],selector)
			else:
				value=get_path(item,selector)
			logger.debug("Value {}".format(value))

			if not value:
				continue

			if isinstance(value,float) or isinstance(value,int):
				out_items.append(item_name+" "+str(value))
			elif isinstance(value,dict):
				logger.debug("Value is a dictionary, nest values")
				for key in value:
					val=value[key]
					if isinstance(val,float) or isinstance(val,int):
						logger.debug("Adding {key}={val}".format(key=key,val=val))
						out_items.append(item_name+'.'+key+" "+str(val))
					elif isinstance(val,str):
						try: 
							val=float(val)
							out_items.append(item_name+'.'+key+" "+str(val))
						except ValueError as verr:
							logger.debug("Ignoring string {key}={val}".format(key=key,val=val))
					else:
						logger.debug("Unknown {key}={val}".format(key=key,val=val))
			if isinstance(value,str):
				raise Exception("Parameters can not be strings")

		logger.debug("Out items {}".format(len(out_items)))
		return "{command}{args}".format(command="\n".join(out_items),args="".join(args[2:]))

	def cmd_map(self,args):
		logger.debug("cmd Map")
		project=args[0]
		## ASSSUME ONLY 1 PROJECT
		project_id,project_name=get_id(project[0])
		self._add_to_map(item_id=project_id,item_name=project_name,item=project[0])
		items=args[1]
		out_items=[]
		if isinstance(items,Tree) and items.data=='selector':
			out_items.append(project_name+"."+"".join(items.children))
		else:
			for item in items:
				item_id,item_name=get_id(item)
				self._add_to_map(item_id=item_id,item_name=item_name,item=item)
				out_items.append(project_name+'.'+item_name)
		logger.debug("Out items {}".format(len(out_items)))
		if len(out_items)>0:
			return "{command}{args}".format(command="\n".join(out_items),args="".join(args[2:]))
		else:
			return ""

	def cmd_list(self,args):
		logger.debug("cmd List")
		items=args[0]

		out_items=[]
		for item in items:
			item_id,item_name=get_id(item)
			self._add_to_map(item_id=item_id,item_name=item_name,item=item)
			out_items.append(item_name)
		if len(out_items)>0:
			return "{command}{args}".format(command=", ".join(out_items),args="".join(args[1:]))
		else:
			return ""

	def cmd_tariff(self,args):
		logger.debug('cmd Tariff')
		tariff_type=args[0].data
		out_items=[]
#		print("context",self._context['data'])
		supply_data=[d for d in self._context['data'] if d['groupKey']=='tourate']
		for supply in supply_data:
			supply_id,supply_name=get_id(supply)
			supply_data=self._data[supply_id]
			self._add_to_map(item_id=supply_id,item_name=supply_name,item=supply)
			if tariff_type.startswith("tariff_sched"):
				if tariff_type=='tariff_sched_weekend':
					schedule_type_key="Weekend"
#					print('there')
				elif tariff_type=='tariff_sched_weekday':
					schedule_type_key='Weekday'
				else:
					raise Exception("Dont understand tariff sched param")
				logger.debug("Generating Tariff Sched")
				for product in ['demand','energy']:
					schedule_key="{product}{type}Sched".format(product=product,type=schedule_type_key)
					schedule=supply_data[schedule_key]
					for month in range(len(schedule)):
						month_key="m{}".format(month+1)
						for hour in range(len(schedule[month])):
							hour_key="h{}".format(hour+1)
							period_key="period{}".format(schedule[month][hour]+1)
							map_item=".".join([supply_name,product,month_key,hour_key,period_key])
							out_items.append(map_item)
			elif tariff_type.startswith("tariff_rate"):
				if tariff_type=='tariff_rate':
					value_key='rate'
				elif tariff_type=='tariff_rate_adj':
					value_key='adj'
				else:
					raise Exception("Dont understand tariff rate param")
				logger.debug("Generating Tariff Rate")
				for product in ['demand','energy']:
					data=supply_data[product+'RateStrux']
					for period in range(len(data)):
						period_key='period{}'.format(str(period+1))
						tier_name='{}RateTiers'.format(product)
						for tier in range(len(data[period][tier_name])):
							tier_key='tier{}'.format(str(tier+1))
							key=".".join([supply_name,product,period_key,tier_key])
							if value_key in data[period][tier_name][tier]:
								value=data[period][tier_name][tier][value_key]
								out_items.append("{} {}".format(key,value))
			else:
				raise Exception("Only know about 2 tariff types")
		return "\n".join(out_items)

	def ao_macro(self,args):
		logger.debug("AO Macro - Inject Info")
		args = [a for a in args if a != '']
		if len(args)==1 and args[0].type=="NL":
			# Empty macro
			logger.debug("Empty macro")
			return ""
		else:
			return "".join(args)
		#return "<-- AO {} - {} -->".format(command,", ".join(out_items))
