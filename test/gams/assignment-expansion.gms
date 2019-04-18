
* Cost by technology + p*0.4 * marginal_cost(gen)*time scale of the AS
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type)*load_follow_cost(gen) +
    anc_time_scale(anc_type)/60*%load_follow_mc%*marginal_cost(gen)*anc_scale_mc_prob(anc_type);



total_wind(time)=sum(wind,p_max_pu_t(time,wind));