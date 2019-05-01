

*****************
*** Overrides ***
*****************
* Pre Init
**********


**********************
*** Initialization ***
**********************
* Primary AO Injection
**********************

** Time definition

set     
    time                  "Time index of model. Currently assumed to be hourly.";

alias (time,t);     

set time /t1*t8760/;

set month /m1*m12/;
set hour /h1*h24/;
set day_of_week /dow1*dow7/;

set weekend(day_of_week) /dow1,dow7/;
set weekday(day_of_week) /dow2*dow6/;

set ch(time) "Time to check" /t1*t8760/;
set chm(month) "Months to check" /m1*m12/;
set m2t(month,time) "Month to time map" /
	m1.t1*t744
/;

** AO Items

* Project
set project /
**ao list project
/;

* Asset
set asset /
**ao list asset
new_solar
new_battery
/;

set site(asset) /
**ao list asset "type startswith asset:land"
/;

set gen(asset) /
**ao list asset "type startswith asset:gen"
**ao list asset "type startswith asset:battery"
new_solar
new_battery
/;

set control_gen(gen) / 
**ao list asset "type startswith asset:gen:combined"
**ao list asset "type startswith asset:gen:combustion"
**ao list asset "type startswith asset:gen:hydro"
**ao list asset "type startswith asset:gen:steam"
/;

set variable_gen(gen) / 
**ao list asset "type startswith asset:gen:renewable"
new_solar
/;
set battery(gen) / 
**ao list asset "type startswith asset:battery"
new_battery
/;

* Data
set data /
**ao list data
/;
set supply(data) /
**ao list data "groupKey == tourate"
/;


** Maps

set project2asset(project,asset) /
**ao map project asset
**ao map project 'new_battery'
**ao map project 'new_solar'
/;

set project2data(project,data) /
**ao map project data
/;

** Parameters

* Fields

set financial_field / 
	discountRate
	federalTaxRate
	stateTaxRate
	inflationRate
	omEsclationRate
	period
/;

set solar_field /
	capacityCost
	capacityPower
	degradationRate
	omCost
/;
set battery_field / 
	capacityCosts
	energyCosts
	power
	duration
	chargeEfficiency
	dischargeEfficiency
/;

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


parameter efficiency_store(gen),efficiency_dispatch(gen),
		soc_min(gen),soc_max(gen)
		p_nom(gen), marginal_cost(gen);

* Data sets , probably a csv
parameter demand(site,time) /
	site_a.t1 10
	site_a.t2 20
/;


** Set parameters

p_nom('new_solar')=10;
p_nom('new_battery')=10;

marginal_cost('new_solar')=0;
marginal_cost('new_battery')=0;

soc_min(battery)=.15;
soc_max(battery)=.95;

efficiency_dispatch('new_battery')=param_battery('project_a','discharge_efficiency');
efficiency_store('new_battery')=param_battery('project_a','charge_efficiency');


*** this is a data object that needs to be encoded by data id
** Supply/Schedule Implementation


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


*****************
*** Overrides ***
*****************
* Pre Model
***********


*************
*** Model ***
*************

Variables	
	totalC 					"Total cost of supplying energy over time frame"

*   Project (Balancing level)
	projectCM(project,month)	"Cost of supplying project for month"
	projectX(project,time)		"Net power of project (assume = 0)"

* 	Supply - Cost
	supply_energyCM(supply,month)			"Cost of energy supply for month"
	supply_demandCM(supply,month)			"Cost of demand charges for month"
	supply_energyCT(supply,time)			"Cost of energy supply at time"
	supply_demandCMP(supply,month,period) 	"Cost of max buy for supply during month-period"

*	Supply - Power
	supplyX(supply,time)				"Net supply at time"
	buyX(supply,time)					"Amount purchased from supply at time"
	sellX(supply,time)					"Amount sold to supply at time"
	max_buyX(supply,month,period)		"Max buy for supply during month-period"

*   Generation
	genC(gen,time)			"Cost of gen at time"
	genCM(gen,month)		"Cost of gen during month"
	genX(gen,time)			"Amount generated from gen at time"

*   Energy Storage	
	storeX(gen,time)		"Amount stored by gen at time (storage unit)"
	dispatchX(gen,time)		"Amount dispatched by gen at time (storage unit)"
	energyX(gen,time)		"Amount of energy at time (storage unit)";

** Bounds
Positive variables genC,genCM,genX,storeX,dispatchX,energyX;
Positive variables supply_energyCM,supply_demandCM,supply_energyCT,supply_demandCMP;
Positive variables buyX,sellX,max_buyX;

projectX.up(project,time)=0;
projectX.lo(project,time)=0;

genX.up(gen,time)=p_nom(gen);

Equations
*   Objective
	total_cost							"total cost of system"

*   Cost components
	project_cost_month(project,month)	"project cost during month"
	energy_cost_month(supply,month)		"energy cost during month"
	demand_cost_month(supply,month)		"demand charge during month"
	demand_cost(supply,month,period)	"demand charge during month-period"
	gen_cost_month(gen,month)			"gen cost during month"
	gen_cost(gen,time)					"gen cost at time"

*   Project Energy Balance
	project_balance(project,time)		"energy balance at project"

*   Supply Balance
	supply_operation(supply,time)				"Supply operation signed"
	supply_max_buy(supply,month,period,time)	"Max buy for supply during month-period"

*   Energy Storage
	storage_balance(battery,time)		"Storage inventory balance"
	battery_power(battery,time)			"Max power of battery over all operation"
	battery_operation(battery,time)		"Battery operational signed"
;

*** Equation Definitions

total_cost..

	totalC =g=
		sum(month$chm(month),
			sum(project,
				projectCM(project,month)
			)
		);


project_cost_month(project,month)$chm(month)..

	projectCM(project,month) =g=
		sum(gen$project2asset(project,gen),
				genCM(gen,month)
			)
		+
		sum(supply$project2data(project,supply),
				supply_energyCM(supply,month)
				+ supply_demandCM(supply,month)
			);


energy_cost_month(supply,month)$chm(month)..

	supply_energyCM(supply,month) =g=12;


demand_cost_month(supply,month)$chm(month)..

	supply_demandCM(supply,month) =g=12
		;


demand_cost(supply,month,period)..

	supply_demandCMP(supply,month,period) =g=12;
** THIS IS THE FUCKING SCHEDULE CONSTRAILTN

gen_cost_month(gen,month)$chm(month)..

	genCM(gen,month) =g= 
		sum(time$(ch(time) and m2t(month,time)),
				genC(gen,time)
			);


gen_cost(gen,time)$ch(time)..

	genC(gen,time) =g=
		marginal_cost(gen)*genX(gen,time);





project_balance(project,time)$ch(time)..

	projectX(project,time) =e=
		sum(gen$project2asset(project,gen),
				genX(gen,time)
			)
		+ 
		sum(supply$project2data(project,supply),
				supplyX(supply,time)
			)
		- sum(site$project2asset(project,site),
			demand(site,time)
			);


supply_operation(supply,time)$ch(time)..

	supplyX(supply,time) =e=
		buyX(supply,time)
		- sellX(supply,time);


** SUCH THAT, TIME IS FOR GIVEN MONTH PERIOD ONLY!!
supply_max_buy(supply,month,period,time)..

	max_buyX(supply,month,period) =g=
		buyX(supply,time);


storage_balance(battery,time)$ch(time)..

	energyX(battery,time+1) =e=
		energyX(battery,time)
		+ storeX(battery,time)*efficiency_store(battery)
		- dispatchX(battery,time);


battery_power(battery,time)$ch(time)..
	
	storeX(battery,time)
	+ dispatchX(battery,time)
	=l= 
	p_nom(battery);


battery_operation(battery,time)$ch(time)..

	genX(battery,time)
	=e=
	storeX(battery,time)
	- dispatchX(battery,time)*efficiency_dispatch(battery);

*****************
*** Overrides ***
*****************
* Pre Solve
***********


*************
*** Solve ***
*************


model site_analysis /
	total_cost
	project_cost_month
	energy_cost_month
	demand_cost_month
	gen_cost_month
	gen_cost
	project_balance
	supply_operation
	supply_max_buy
	storage_balance
	battery_power
	battery_operation
/;

solve site_analysis using lp minimizing totalC;



*****************
*** Overrides ***
*****************
* Post Solve
************


******************
*** Extraction ***
******************
* Data exfil
************