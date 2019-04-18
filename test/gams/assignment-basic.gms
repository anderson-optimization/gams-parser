total_wind(time)=sum(wind,p_max_pu_t(time,wind));

total_solar(time)=prod((solar,x2),p_max_pu_t(time,solar,x2));

marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) * load_follow_cost(gen);
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) + load_follow_cost(gen);
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) - load_follow_cost(gen);
marginal_cost_anc(gen,anc_type)=anc_scale_follow_cost(anc_type) / load_follow_cost(gen);

