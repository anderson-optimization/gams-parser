
## TODO

### Gams Parser

- Add transformer to create structured representation of model in gams
- Output information for pretty print in UI

	- Symbol definitions ( sets, parameters, variables, equations )
	- line of statement - the actual string
	- Index list
	- Description

- Wrap in task to interact with UI

### AO Injector

- Create inject syntax DSL
- Wrap in task system, get project/asset information from event
- Use input information to inject based on inject DSL mapping


## TESTS

python $( which nosetests ) -v --nocapture test/*.py
