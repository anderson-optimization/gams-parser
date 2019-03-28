total_wind(time)=sum(wind,p_max_pu_t(time,wind));


p_max_pu_t(time,solar)=sum(sr$solar_sr(solar,sr),p_max_pu_t_sr(time,sr));

total_solar(time)=sum(solar,p_max_pu_t(time,solar));

marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) * load_follow_cost(gen);
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) + load_follow_cost(gen);
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) - load_follow_cost(gen);
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) / load_follow_cost(gen);
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) + %load_follow_mc%;


* Cost by technology + p*0.4 * marginal_cost(gen)*time scale of the AS
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type)*load_follow_cost(gen) +
    anc_time_scale(anc_type)/60*%load_follow_mc%*marginal_cost(gen)*anc_scale_mc_prob(anc_type);



total_wind(time)=sum(wind,p_max_pu_t(time,wind));


$if set load_scale p_set_t(time,load)=%load_scale%*p_set_t(time,load);


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


