
****************************
*** Model Initialization ***
**************************** 


************
*** Time ***
************

$ontext
The model can be temporally decomposed in a few ways.
$offtext

set     
    time                  "Time index of model. Currently assumed to be hourly.";

alias (time,t);     

set
*   Date time map
    datetime_comp         "Datetime components used to map a time index to a real datetime." 
                            /year,month,day,hour,minute,second/
    year                  "Years possible in the simulat" /y2018*y2028/
    month                 "Months of the year" /m1*m12/
    m2t(month,time)       "Map month to time"

*   Solve subset of time
    ch(time)              "These time elements are included in the current solve (includes look ahead)." 
    ch_store(time)        "These time elements are saved after the current solve (excludes look back/ahead)"
    ch_all(time)         "These time elements include both the look ahead and look back period"

*   Solve in larger window usings look ahead, look back
    ch_window(time,t)       "This set maps a single time element to include its lookahead window"
    ch_back_window(time,t)  "This set maps a single time element to include its lookback window"
    lookbacktime(time,t)    "Look back time exclusive of current time" 
    lookaheadtime(time,t)   "Look ahead time exclusive of current time" 

*   Solve many subsets in blocks
    block                           "A block represents a chunk of time to solve together"
    check_block(block)              "Blocks to solve in single gams run"
    block_time(block,time)          "Maps blocks to time elements"
    block_window(block,time)        "Map blocks to time with look ahead"
    block_back_window(block,time)    "Map blocks to time with look back"
    ch_all_time(time,t)             "All time elements to check in gams run"
    run_time(time)                  "Time (excluding lookback/ahead) included in all of run"
    run_time_window(time)           "Time (including lookahead) included in all of run"
    run_time_all(time)           "Time (including lookback/ahead) included in all of run"
    run_time_first(time)            "First time period of run"
    run_time_last(time)             "Last time period of run";



parameter   date(time)                        "Maps time to gams internal date format"
            datetime_map(time,datetime_comp)  "Maps time to datetime components";

*date(time) is deprecated, transition to datetime_map

$include %gamsfolder%em_init_time.inc


************
*** Sets ***
************

set     
*   Components
    bus                     "Fundamental node of the network to which loads, generators, and transmission lines attach." 
    branch                  "A branch in the network connects two busses and include transmission and transformers." 
    passive(branch)         "Passive branches represent AC power lines within a synchronous grid and are not directly controllable."
    transformer(branch)     "Transformers represent 2-winding transformers that convert AC power from one voltage level to another."
    dc(branch)              "A HVDC branch is a controllable link between two nodes"
    gen                     "Generators attach to a single bus and can feed in power."
    commit(gen)             "commitable gens * This is actually gens with ramp rate>1 hour"
    operational(gen)        "Operational generators can be controlled and used to respond to variations in demand"
    wind(gen)               "Wind generators have a max generation corresponding to a wind resource and can be curtailed"
    solar(gen)              "Solar generators have a max generation corresponding to a solar resource and can be curtailed"
    thermal(gen)            "Thermal generators are an operational resource with energy_source inputs (not used currently)"
    slow_commit(gen)               "Slow generators with min up/down > 1 hour"
    energy_sourceuse(gen)            "Generators that can use energy_source use constraints"
    hydro(gen)              "Hydro generators can be complicated and I am not doing anything with them currently"
    battery(gen)            "Batteries can be charged, discharged, and have a state of charge"
    load                    "Loads connect to a bus and represent a fixed demand on the system" 
    sub_network             "Sub-networks are subsets of buses and passive branches (i.e. lines and transformers) that are connected. as a synchronous grid"

*   Gen Info
    prime_mover             "Prime mover according to EIA"
    technology              "Technology according to EIA"
    energy_source           "Energy source according to EIA"            

*   Fuel Information
    fuel                    "Fuel source we have prices for"
    sr                      "Solar resource"  /sr1*sr25/

*   EIA Mappings
    eia_plant               "Plant from EIA-860"
    eia_gen                 "Gen from EIA-860"
;

alias(technology,tech);

$include %gamsfolder%em_init_sets.inc

* Operational set is messed up, should be no wind and solar
operational(gen)$(wind(gen) or solar(gen))=No;



****************
*** Mappings ***
****************

set 
*   Sub networks of synchronized grids
    bus_sub_network(bus,sub_network)    "Map bus to sub network"

*   Nodal Locations
    load_bus(load,bus)          "Map load to bus" 
    gen_bus(gen,bus)            "Map generatpr to bus"
    branch_bus0(branch,bus)     "Map branch to bus0" 
    branch_bus1(branch,bus)     "Map branch to bus1" 

*   Gen Info
    gen_energy_source(gen,energy_source) "Generator energy source for power"
    gen_startup_source(gen,energy_source) "Generator energy source for startup"
    gen_prime_mover(gen,prime_mover) "Generator prime mover for power"
    gen_technology(gen,technology) "Generator technology"

*   EIA Maps
    eia_plant_eia_gen(eia_plant,eia_gen)    "EIA Plant and EIA Generator"
    gen_eia_plant(gen,eia_plant)            "Generator to EIA Plant"
    gen_eia_gen(gen,eia_gen)                "Generator to EIA Gen"

*   Solar
    solar_sr(solar,sr)                      "Solar to solar resource"
;


$include %gamsfolder%em_init_maps.inc


solar_sr(solar,sr)=1$(ord(solar)=ord(sr));



*******************
*** Ancillaries ***
*******************


set anc_type                    "Ancillary service types" /reg_up,reg_down,res_spin,res_nonspin/;

alias (anc_type, anc_type2);

set anc_type_contrib(anc_type,anc_type2) "Ancillary contribution denotes which type of ancillaries contribute to teh requirements" 
    /
        reg_up.reg_up
        reg_down.reg_down
        res_spin.res_spin
*        res_nonspin.res_spin
        res_nonspin.res_nonspin
    /;

set anc_type_gen_on(anc_type)     "Ancillary provided when gen is on" /reg_up,reg_down,res_spin/;
set anc_type_gen_off(anc_type)     "Ancillary provided when gen is off" /res_nonspin/;

parameter anc_time_scale(anc_type) "Time scale of ancillary type (minutes)" /
reg_up  5
reg_down 5
res_spin 10
res_nonspin 30
/;



******************
*** Generators ***
******************

parameters
    p_nom(gen)              "Nominal power of generator (MW)"
    ramp_limit_up(gen)      "Maximum ramp up per time unit (MW)"
    ramp_limit_down(gen)    "Maximum ramp down per time unit (MW)"
    status(gen)             "Status of generator for current run [0/1]"

*   Expandable gens
    capital_cost(gen)       "Capital cost of generator ($/MW)"

*   Cost info breakdown
    marginal_cost(gen)              "Marginal cost per unit energy created ($/MWh)"
    average_heatrate(gen)           "Average heatrate of generator (Mbtu/MWh)"
    average_energy_source_cost(gen) "Average energy_source cost for energy_source used by generator ($/Mbtu)"
    variable_om(gen)                "variable operation and maintainence ($/MWh)"
    startup_energy_source(gen)      "Startup energy_source used (Mbtu)"
    startup_other_cost(gen)         "Startup cost ($)"
    load_follow_cost(gen)           "Load following cost ($/MW)"
    operational_cost(gen)           "Operational cost of gen when running ($/hr)"
    marginal_cost_anc(gen,anc_type) "Marginal cost for providing ancillaries ($/MW)"
    anc_capability(gen,anc_type)    "Ancillary capabilities of generator (MW)"

*   Thermal generators

*   Commitable Generators
    min_up_time(gen)            "Min up of generator (t)"
    min_down_time(gen)          "Min down of generator (t)"
    ramp_limit_start_up(gen)    "Start up ramp rate (MW/t)"
    ramp_limit_shut_down(gen)   "Shut down ramp rate (MW/t)"
    start_up_cost(gen)          "Start up cost ($)"
    shut_down_cost(gen)         "Shut down cost ($)"
    p_min_pu(gen)               "Minimum generation while on"
    p_max_pu(gen)               "Maximum generation while on"

*   Wind/Solar
    p_max_pu_t(time,gen)        "Max generation per unit capacity by time [0,1]"

*   Battery
    duration(gen)               "Duration of battery (t)"
    energy_capacity(gen)        "Energy capacity (MWh)"
    soc_max_pu(gen)             "State of charge max [0,1]"
    soc_min_pu(gen)             "State of charge min [0,1]"
    cycle_depth_pu(gen)         "Cycle depth [0,1]"
    lifetime_cycles(gen)        "Lifetime cycles used to calculate cost of cycle"
    cycle_cost(gen)             "Cycle cost of generator ($/cycle)"
    efficiency_store(gen)       "Efficiency of storing energy [0,1]"
    efficiency_dispatch(gen)    "Efficiency of dispatching energy [0,1]"
;

$include %gamsfolder%em_init_parameters_gen.inc

status(gen)=1;


**************************
*** Capacity Expansion ***
**************************

* Bootstrap new gens if CE model

$if %modeltype% == 'ce' $include %gamsfolder%ce_init.inc


** Oversupply, we must have too many gens or soemthing ??
p_nom(gen)$gen_technology(gen,'natural_gas_steam_turbine')=%natural_gas_scale%*p_nom(gen);
p_nom(gen)$gen_technology(gen,'natural_gas_fired_combustion_turbine')=%natural_gas_scale%*p_nom(gen);
p_nom(gen)$gen_technology(gen,'natural_gas_fired_combined_cycle')=%natural_gas_scale%*p_nom(gen);

*** Marginal Cost Corrections

marginal_cost(wind) = 0 - %wind_subsidy%;

* Add some more variation, seems like there is a few cheaper gens on the system and some more expensive gens

marginal_cost(operational)=marginal_cost(operational)*
    normal_scale(%marginal_cost_mean%,%marginal_cost_std%,%marginal_cost_min%,%marginal_cost_max%);



*** Ramp Rates

parameter ramp_rate_technology(technology) "%/hour ramp rate mean" /
conventional_steam_coal 0.042
natural_gas_steam_turbine 0.072
natural_gas_fired_combustion_turbine 0.064
natural_gas_fired_combined_cycle 0.086
natural_gas_internal_combustion_engine 0.11
petroleum_coke 0.079
nuclear 0.041
all_other 0.09
other_gases 0.072
wood_wood_waste_biomass 0.042
/;


ramp_limit_up(gen) = param_tech(ramp_rate_technology,gen)*p_nom(gen);
ramp_limit_down(gen) = param_tech(ramp_rate_technology,gen)*p_nom(gen);

ramp_limit_up(gen)$(not ramp_limit_up(gen))=0.04*p_nom(gen);
ramp_limit_down(gen)$(not ramp_limit_down(gen))=0.04*p_nom(gen);


* These values seem to be underestimated, scale
ramp_limit_up(gen)=ramp_limit_up(gen)*%ramp_rate_scale%;
ramp_limit_down(gen)=ramp_limit_down(gen)*%ramp_rate_scale%;


*parameter ramp_limit_pu(gen);
*ramp_limit_pu(gen)$p_nom(gen)=ramp_limit_up(gen)/p_nom(gen);
*display ramp_limit_pu;



*** Committable gens, min up/min down

p_min_pu(gen)=0;
p_max_pu(gen)=1;

parameter min_capacity_technology(technology) /
conventional_steam_coal 0.4
natural_gas_steam_turbine 0.4
natural_gas_fired_combustion_turbine 0.4
natural_gas_fired_combined_cycle 0.4
natural_gas_internal_combustion_engine 0.25
nuclear 0.5
/;

p_min_pu(gen)=param_tech(min_capacity_technology,gen);


$if not set ramp_rate_startup ramp_limit_start_up(gen) = p_min_pu(gen)*p_nom(gen);
$if set ramp_rate_startup ramp_limit_start_up(gen) = p_min_pu(gen)*p_nom(gen)-ramp_limit_up(gen);
ramp_limit_shut_down(gen) = p_min_pu(gen)*p_nom(gen);
*ramp_limit_shut_down(gen) = p_nom(gen);

parameter min_up_time_technology(technology) /
conventional_steam_coal 6
natural_gas_steam_turbine 0
natural_gas_fired_combustion_turbine 0
natural_gas_fired_combined_cycle 2
natural_gas_internal_combustion_engine 0
nuclear 8
/;
parameter min_down_time_technology(technology) /
conventional_steam_coal 4
natural_gas_steam_turbine 0
natural_gas_fired_combustion_turbine 0
natural_gas_fired_combined_cycle 2
natural_gas_internal_combustion_engine 0
nuclear 4
/;

min_up_time(gen)=param_tech(min_up_time_technology,gen);
min_down_time(gen)=param_tech(min_down_time_technology,gen);


slow_commit(gen)$(min_up_time(gen)>1)=Yes;


*** Start up Costs

parameter startup_energy_source_technology(technology) /
conventional_steam_coal 10
natural_gas_steam_turbine   7
natural_gas_fired_combustion_turbine    1.2
natural_gas_fired_combined_cycle    0.2
natural_gas_internal_combustion_engine  0.2
petroleum_coke  5
nuclear 5
other_gases 5
wood_wood_waste_biomass 5
/;

parameter startup_other_cost_technology(technology) /
conventional_steam_coal 7.98
natural_gas_steam_turbine 6.86
natural_gas_fired_combustion_turbine 1.5
natural_gas_fired_combined_cycle 0.5
natural_gas_internal_combustion_engine 0.5
petroleum_coke 5
nuclear 10
all_other 5
other_gases 5
wood_wood_waste_biomass 5
/;

startup_energy_source(gen) = param_tech(startup_energy_source_technology,gen);
startup_other_cost(gen) = param_tech(startup_other_cost_technology,gen);

start_up_cost(gen)=(startup_energy_source(gen)*average_energy_source_cost(gen)+startup_other_cost(gen))*p_nom(gen)
    *normal_scale(%startup_cost_mean%,%startup_cost_std%,%startup_cost_min%,%startup_cost_max%);

parameter operational_cost_year_technology(technology) "Fixed O&M ($/kw-yr)"/
conventional_steam_coal 45
natural_gas_steam_turbine   10
natural_gas_fired_combustion_turbine    12
natural_gas_fired_combined_cycle    10
natural_gas_internal_combustion_engine  10
petroleum_coke  20
nuclear 99
other_gases 10
wood_wood_waste_biomass 50
/;

parameter operational_cost_technology(technology) "Fixed O&M ($/MW)";

operational_cost_technology(technology)=operational_cost_year_technology(technology)*1000/8760;

operational_cost(gen) = p_nom(gen)*param_tech(operational_cost_technology,gen);

operational_cost(gen) = operational_cost(gen)
    *normal_scale(%operational_cost_mean%,%operational_cost_std%,%operational_cost_min%,%operational_cost_max%);




*** Ancillary Capabilities

* By default, scale ramp rate by time scale
anc_capability(gen,anc_type)=
    ramp_limit_up(gen)*anc_time_scale(anc_type)/60;

* Ensure certain categories are realistic
anc_capability(wind,anc_type)=0;
anc_capability(solar,anc_type)=0;
anc_capability(gen,'reg_up')$gen_technology(gen,'nuclear')=0;
anc_capability(gen,'reg_down')$gen_technology(gen,'nuclear')=0;
anc_capability(gen,'res_nonspin')$gen_technology(gen,'nuclear')=0;
anc_capability(gen,'reg_up')$gen_technology(gen,'conventional_steam_coal')=0;
anc_capability(gen,'reg_down')$gen_technology(gen,'conventional_steam_coal')=0;
anc_capability(gen,'res_nonspin')$gen_technology(gen,'conventional_steam_coal')=0;
anc_capability(gen,'res_nonspin')$gen_technology(gen,'natural_gas_steam_turbine')=0;
anc_capability(gen,'res_nonspin')$gen_technology(gen,'natural_gas_fired_combined_cycle')=%natural_gas_cc_anc%*anc_capability(gen,'res_nonspin');

$ontext
natural_gas_steam_turbine reg up / reg down / nonspin
conventional_steam_coal
natural_gas_fired_combustion_turbine
natural_gas_internal_combustion_engine
natural_gas_fired_combined_cycle
petroleum_coke
nuclear
all_other
other_gases
wood_wood_waste_biomass
onshore_wind_turbine
batteries
solar_photovoltaic
conventional_hydroelectric
nan
$offtext



*** Load Follow Cost

set follow_cost_stat /mean,std,min,max/;

* From NREL Cycle cost - These are lower bound figures


parameter load_follow_cost_tech(technology);
load_follow_cost_tech(technology)=
    test
    *normal_scale(%operational_cost_mean%,%operational_cost_std%,%operational_cost_min%,%operational_cost_max%);

* Adjust for missing upper bound data
load_follow_cost(gen)=param_tech(load_follow_cost_tech,gen);


parameter anc_scale_follow_cost(anc_type) /
reg_up  0.75
reg_down 0.75
res_spin 1
res_nonspin 0.2
/;

parameter anc_scale_mc_prob(anc_type) "Probability of calling on resource (which adds marginal cost to bid)" /
reg_up  1
reg_down 0.25
res_spin 0.5
res_nonspin 0.25
/;


* Cost by technology + p*0.4 * marginal_cost(gen)*time scale of the AS
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type)*load_follow_cost(gen) +
    anc_time_scale(anc_type)/60*%load_follow_mc%*marginal_cost(gen)*anc_scale_mc_prob(anc_type);



parameter total_wind(time);
parameter total_solar(time);

total_wind(time)=sum(wind,p_max_pu_t(time,wind));

*parameter p_max_pu_t_solar(t) /
*$ondelim
*$include %datafolder%gen/p_max_pu_solar.csv
*$offdelim
*/;

p_max_pu_t(time,solar)=sum(sr$solar_sr(solar,sr),p_max_pu_t_sr(time,sr));

total_solar(time)=sum(solar,p_max_pu_t(time,solar));



****************
*** Branches ***
****************

parameters 
    s_nom(branch)       "Nominal capacity of branch"
    x_pu_eff(branch)    "Reactance x per unit (s_nom) effective"
    r_pu_eff(branch)    "Resistance r per unit (s_nom) effective"
    ptdf(branch,bus)    "Power transfer distribution factors"
;

$include %gamsfolder%em_init_parameters_branch.inc





*************
*** Loads ***
*************

parameters
    p_set_t(time,load)          "Power load"
    anc_system_req(anc_type)    "Anc requirements as a percent of total load"
    anc_set_t(time,anc_type)    "Ancillary system requirements by time"
    total_load(time)            "Total system load"
    net_load(time)            "Total system load"
;

parameter anc_system_req_percent_load(anc_type) /
reg_up      0.01
reg_down    0.01
res_spin    0.01
res_nonspin 0.02
/;
parameter anc_system_req_constant(anc_type) /
reg_up      0
reg_down    0
res_spin    900
res_nonspin 800
/;


$include %gamsfolder%em_init_parameters_load.inc


$if set load_scale p_set_t(time,load)=%load_scale%*p_set_t(time,load);

$if set load_scale total_load(time)=sum(load,p_set_t(time,load));

$if set load_scale net_load(time)=total_load(time)-total_wind(time)-total_solar(time);

$if set load_scale anc_set_t(time,anc_type)=anc_system_req_percent_load(anc_type)*net_load(time)+anc_system_req_constant(anc_type);





******************
*** Violations ***
******************

* Relax problem by allowing violations for a cost


scalar  load_shed_cost,
        anc_violation_cost,
        flow_violation_cost;

load_shed_cost=%load_violation%;
anc_violation_cost=%anc_violation%;
flow_violation_cost=%flow_violation%;


***************
*** Forward ***
*************** 

* Override forward information

$if set forward_run $include %gamsfolder%em_init_forward.inc


