
parameter   date(time)                        "Maps time to gams internal date format"
            datetime_map(time,datetime_comp)  "Maps time to datetime components";

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


Parameter Netreturns(products)  'Net returns per unit produced'
              / Chairs 19, Tables 50, Dressers 75 /
          Endowments(resources) 'Amount of each resource available'
              / RawWood 700, Labor 1000, WarehouseSpace 240 /;
