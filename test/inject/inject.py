from gams_parser import GamsParser
import json

def test_inject_list():
	gp = GamsParser('./test/gams/inject-basic.gms')
	with open('./test/ao/scenario-context.json') as in_file:
		data=json.load(in_file)
		#print(data)
		print("Inject data")
		new_model=gp.inject(context=data)
		print("Output")
		print(new_model)

def test_inject_filtered():
	gp = GamsParser('./test/gams/inject-filtered.gms')
	with open('./test/ao/scenario-context.json') as in_file:
		data=json.load(in_file)
		#print(data)
		print("Inject data")
		new_model=gp.inject(context=data)
		print("Output")
		print(new_model)
