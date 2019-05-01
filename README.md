
# GAMS Parser

This python library uses [lark](https://github.com/lark-parser/lark) to parse the algebraic modeling language [GAMS](https://www.gams.com/).  

## Goals

Interested in two directions.  Optional 3rd

1. Gather rich data on structure of model in a gams file.
2. Inject custom defintions and data into gams files based upon a DSL.
3. [Optional] Gather defined data from model using python api.
	- This is probably outside the scope of this library as it requires `GAMS` as a dependency.


## GAMS to AST Model [ Parser ]

This accomplishes goal 1.

Create structure model from GAMS code.


SHORT PARAGRAPH ON THIS FUNCTIONALITY

HOW TO USE HERE

### Examples

EXAMPLES HERE

## AO Injector 

This accomplishes goal 2.

Inject GAMS code into gams file using AO context item.

SHORT PARAGRAPH ON THIS FUNCTIONALITY

HOW TO USE HERE

### Examples


#### List and map items

Template file

```
* Project
set project /
**ao list project
/;

set asset /
**ao list asset
new_solar
new_battery
/;

set gen(asset) /
**ao list asset "type startswith asset:gen"
**ao list asset "type startswith asset:battery"
new_solar
new_battery
/;


set project2asset(project,asset) /
**ao map project asset
/;

set project2data(project,data) /
**ao map project data
/;
```

Output

```
* Project
set project /
SiteAProject
/;

* Asset
set asset /
SiteA_Parcel, ArcelormittalClevelandInc_GENC
new_solar
new_battery
/;

set gen(asset) /
ArcelormittalClevelandInc_GENC
new_solar
new_battery
/;

set project2asset(project,asset) /
SiteAProject.SiteA_Parcel
SiteAProject.ArcelormittalClevelandInc_GENC
SiteAProject.new_battery
SiteAProject.new_solar
/;

set project2data(project,data) /
SiteAProject.SiteALoad
SiteAProject.SiteA_TOURates
/;
```

#### Params

Template

```
parameter param_financial(project,financial_field) /
**ao param project 'step.financial.parameter.simplefinance'
/;

parameter param_solar(project,solar_field) /
**ao param project 'step.solar.parameter.solar'
/;

** SOC min/max????
parameter param_battery(project,battery_field) /
**ao param project 'step.battery.parameter.batterycapitalcost'
**ao param project 'step.battery.parameter.batterycharacter'
**ao param project 'step.battery.parameter.batterysize'
/;
```

Output

```
parameter param_financial(project,financial_field) /
SiteAProject.stateTaxRate 0.05
SiteAProject.inflationRate 0.03
SiteAProject.period 25
SiteAProject.federalTaxRate 0.25
SiteAProject.omEscalationRate 0.02
SiteAProject.discountRate 0.08
/;

parameter param_solar(project,solar_field) /
SiteAProject.degradationRate 2
SiteAProject.capacityCost 1500
SiteAProject.omCost 2
SiteAProject.capacityPower 5
/;

** SOC min/max????
parameter param_battery(project,battery_field) /
SiteAProject.energyCosts 1500
SiteAProject.capacityCosts 1500
SiteAProject.dischargeEfficiency 0.95
SiteAProject.chargeEfficiency 0.95
SiteAProject.duration 2
/;
```

#### Tariff Structure

Template

```
set product /energy,demand/;
set period /period1*period10/;
set tier /tier1*tier10/;

parameter product_rate(supply,product,period,tier) "Rate of energy/demand cost ($/kWh and $/kW)";
parameter product_adj(supply,product,period,tier) "Rate of adjustment ($/kWh and $/kW)";

set weekday_schedule(supply,product,month,hour,period);
set weekend_schedule(supply,product,month,hour,period);


** Tariff definition

parameter product_rate(supply,product,period,tier) /
**ao tariff product_rate
/;
parameter product_adj(supply,product,period,tier) /
**ao tariff product_adj
/;

set weekend_schedule(supply,product,month,hour,period) /
**ao tariff weekend_schedule
/;

set weekday_schedule(supply,product,month,hour,period) /
**ao tariff weekend_schedule
/;
```

Output

```
set product /energy,demand/;
set period /period1*period10/;
set tier /tier1*tier10/;

parameter product_rate(supply,product,period,tier) "Rate of energy/demand cost ($/kWh and $/kW)";
parameter product_adj(supply,product,period,tier) "Rate of adjustment ($/kWh and $/kW)";

set weekday_schedule(supply,product,month,hour,period);
set weekend_schedule(supply,product,month,hour,period);


** Tariff definition

parameter product_rate(supply,product,period,tier) /
supply1.demand.period1.tier1 0
supply1.demand.period2.tier1 19.8
supply1.demand.period3.tier1 17
supply1.energy.period1.tier1 0.0584
supply1.energy.period2.tier1 0.0321
supply1.energy.period3.tier1 0.04
supply1.energy.period4.tier1 0.032
/;
parameter product_adj(supply,product,period,tier) /
supply1.demand.period1.tier1 0
supply1.demand.period2.tier1 0
supply1.demand.period3.tier1 0
supply1.energy.period1.tier1 0
supply1.energy.period2.tier1 0
supply1.energy.period3.tier1 0
supply1.energy.period4.tier1 0
/;

set weekend_schedule(supply,product,month,hour,period) /
supply1.demand.m1.h1.period1
supply1.demand.m1.h2.period1
supply1.demand.m1.h3.period1
supply1.demand.m1.h4.period1
supply1.demand.m1.h5.period1
supply1.demand.m1.h6.period1
supply1.demand.m1.h7.period1
supply1.demand.m1.h8.period1
supply1.demand.m1.h9.period1
supply1.demand.m1.h10.period1
supply1.demand.m1.h11.period1
supply1.demand.m1.h12.period1
supply1.demand.m1.h13.period1
supply1.demand.m1.h14.period1
supply1.demand.m1.h15.period1
supply1.demand.m1.h16.period1
supply1.demand.m1.h17.period1
* etc...
/;
```


## Grammar

- The current grammar is focused on capturing all `GAMS` syntax as long as it is valid and less concerned about catching invalid syntax.
- The current grammar is built to gather data related to symbol definitions.  As such, other parts of the grammar may be not accurate.

### Difficulties

- Gams operates on two passes through the input files.  Compiler statements are done before execution and are used to directly include gams code into a parent file or add/remove specific statements.
- Lark parses the gams file in one pass and is a somewhat hybrid of compiler/execution syntax.  This leads to set values possibly containing only include statements, whereas `GAMS` would check to ensure these are actual set values at execution time as well.

### Gams Syntax

[https://www.gams.com/latest/docs/UG_SetDefinition.html](https://www.gams.com/latest/docs/UG_SetDefinition.html)

### ISSUES


The expression grammar doesn't obey order of operations for math.  use this calculater as reference for parsing structure. [https://github.com/lark-parser/lark/blob/master/examples/calc.py](https://github.com/lark-parser/lark/blob/master/examples/calc.py)


## Tests

The `test/gams` folder contains sample gams syntax that can be used to test a grammar file to ensure it captures `GAMS` fairly complex syntax.  

```
make test
make test FLAGS="--nocapture --nologcapture"
```
