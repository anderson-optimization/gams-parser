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
		new_model=gp.inject(context=data,data=tariff)
		print("Output")
		print(new_model)
