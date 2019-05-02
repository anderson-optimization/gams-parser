from gams_parser import GamsParser
import json

import pprint

import logging
logging.basicConfig(level=logging.DEBUG)

def test_inject_data_gen():
	gp = GamsParser('./test/gams/inject-datagen.inc')
	with open('./test/ao/scenario-context.json') as in_file, \
			open('./test/ao/demand.json') as demand_file, \
			open('./test/ao/nrel-sam-gen.json') as gen_file:
		data=json.load(in_file)
		demand=json.load(demand_file)
		gen=json.load(gen_file)
		print("Inject data")
		d_map={
			"nrel-sam-gen": gen,
			"-LXKR3vVaHl1b3lDunJL": demand
		}
		new_model,inject_map=gp.inject(context=data,data=d_map)
		print("Output")
		#print(new_model)
		inject_simple=[{
			"id": item['item_id'],
			"name": item['item_name'],
			"type": item['item']['type'],
			"rn": item['item']['rn']
		} for item in inject_map]
		pprint.pprint(inject_simple)

		with open('tmp/output-gen.gms','w') as out_file:
			out_file.write(new_model)

def test_inject_data_demand():
	gp = GamsParser('./test/gams/inject-datademand.inc')
	with open('./test/ao/scenario-context.json') as in_file, \
			open('./test/ao/demand.json') as demand_file, \
			open('./test/ao/nrel-sam-gen.json') as gen_file:
		data=json.load(in_file)
		demand=json.load(demand_file)
		gen=json.load(gen_file)
		print("Inject data")
		d_map={
			"nrel-sam-gen": gen,
			"-LXKR3vVaHl1b3lDunJL": demand
		}
		new_model,inject_map=gp.inject(context=data,data=d_map)
		print("Output")
		#print(new_model)
		inject_simple=[{
			"id": item['item_id'],
			"name": item['item_name'],
			"type": item['item']['type'],
			"rn": item['item']['rn']
		} for item in inject_map]
		pprint.pprint(inject_simple)

		with open('tmp/output-demand.gms','w') as out_file:
			out_file.write(new_model)