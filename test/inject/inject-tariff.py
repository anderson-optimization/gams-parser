from gams_parser import GamsParser
import json

import logging
logging.basicConfig(level=logging.DEBUG)

def test_inject_tariff():
	gp = GamsParser('./test/gams/inject-tariff.gms')
	with open('./test/ao/scenario-context.json') as in_file, \
			open('./test/ao/tariff.json') as tariff_file:
		data=json.load(in_file)
		tariff=json.load(tariff_file)
		print(tariff.keys())
		print("Inject data")
		d_map={
			"-LXKLG1sepBvV6cTX0EN":tariff
		}
		new_model,inject_map=gp.inject(context=data,data=d_map)
		print("Output")
		print(new_model)
