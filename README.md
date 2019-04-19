
# GAMS Parser

This python library uses [lark](https://github.com/lark-parser/lark) to parse the algebraic modeling language [GAMS](https://www.gams.com/).  

## Goals

Interested in two directions.  Optional 3rd

1. Gather rich data on structure of model in a gams file.
2. Inject custom defintions and data into gams files based upon a DSL.
3. [Optional] Gather defined data from model using python api.
	- This is probably outside the scope of this library as it requires `GAMS` as a dependency.

## Grammar

- The current grammar is focused on capturing all `GAMS` syntax as long as it is valid and less concerned about catching invalid syntax.
- The current grammar is built to gather data related to symbol definitions.  As such, other parts of the grammar may be not accurate.

### Difficulties

- Gams operates on two passes through the input files.  Compiler statements are done before execution and are used to directly include gams code into a parent file or add/remove specific statements.
- Lark parses the gams file in one pass and is a somewhat hybrid of compiler/execution syntax.  This leads to set values possibly containing only include statements, whereas `GAMS` would check to ensure these are actual set values at execution time as well.

### Gams Syntax

[https://www.gams.com/latest/docs/UG_SetDefinition.html](https://www.gams.com/latest/docs/UG_SetDefinition.html)


## Tests

The `test/gams` folder contains sample gams syntax that can be used to test a grammar file to ensure it captures `GAMS` fairly complex syntax.  

```
make test
make test FLAGS="--nocapture"
```

## TODO

### Grammar

The expression grammar doesn't obey order of operations for math.  use this calculater as reference for parsing structure. [https://github.com/lark-parser/lark/blob/master/examples/calc.py](https://github.com/lark-parser/lark/blob/master/examples/calc.py)

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

