
from lark import Lark
import os

from .tree_injector import TreeInjector
from .tree_to_model import TreeToModel

import logging
logger = logging.getLogger('gams_parser')


dirname = os.path.dirname(__file__)
grammar_gams = os.path.join(dirname, 'grammar/gams.lark')
grammar_ao_inject = os.path.join(dirname, 'grammar/ao_inject.lark')


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

	def inject(self,context=None,run=None,data=None):
		logger.debug("GamsParser : Inject : 1. Parse")
		self.text+="\n"
		pt= lark_ao_inject.parse(self.text)
		print("Parse Tree")
		print(pt.pretty())
		logger.debug("GamsParser : Inject : 2. Transform")
		TI=TreeInjector(context,data=data)
		new_model,inject_map=TI.transform(pt)
		return new_model,inject_map

	def parse(self):
		return lark_gams.parse(self.text)

	def transform(self):
		parse_tree=lark_gams.parse(self.text)
		model=TreeToModel().transform(parse_tree)
		model.cross_reference()
		model.reference_lines(self.text)
		return model


