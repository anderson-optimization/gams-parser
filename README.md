
# GAMS Parser

This python library uses `lark` to parse the algebraic modeling language `GAMS`.  

## Goals

Interested in two directions.

1. Gather rich data on model in a gams file.
2. Inject custom defintions and data into gams files based upon a DSL.

### Grammer

- The current grammer is focused on capturing all `GAMS` syntax as long as it is valid and less concerned about catching invalid syntax.
- The current grammer is built to gather data related to symbol definitions.  As such, other parts of the grammer may be not accurate.


## Tests

The `test/gams` folder contains sample gams syntax that can be used to test a grammer file to ensure it captures `GAMS` fairly complex syntax.  

```
python $( which nosetests ) -v --nocapture test/*.py
```

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

