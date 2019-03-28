
****************************
*** Model Initialization ***
**************************** 


*date(time) is deprecated, transition to datetime_map

$include %gamsfolder%em_init_time.inc
************
*** Time ***
************

$ontext
The model can be temporally decomposed in a few ways.
block denotes a subset of time that should be solved together.  This allows a user to change from solving
    a 4 hour block of time to a month at a time.  The amount of time that can be solved together
    depends on the complexitity of the model.
ch(time) is used to denote the time that should be solved in the current 
$offtext

parameter anc_time_scale(anc_type) "Time scale of ancillary type (minutes)" /
reg_up  5
reg_down 5
res_spin 10
res_nonspin 30
/;


Set       products  'Items produced' 
              / Chairs, Tables, Dressers /;

set time "time" /t1*t4/
    months /m1*m5,m7*m10/;

alias (time,t2);

set product_sold(products,time) "products sold";

Set       products_no_description  
              / Chairs, Tables, Dressers /;

Parameter Netreturns(products)  'Net returns per unit produced'
              / Chairs 19, Tables 50, Dressers 75 /;              


parameter   date(time)                        "Maps time to gams internal date format"
            datetime_map(time,datetime_comp)  "Maps time to datetime components";

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

scalar  load_shed_cost,
        anc_violation_cost,
        flow_violation_cost;