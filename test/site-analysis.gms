

set projects /project_a/;

set steps /land,demand,supply,solar,battery,financial/;


set fields /capacity_cost,capacity/;






set assets /site_a/;

set site(assets) /site_a/;



parameter demand(site)
		  supply_rates(site);


parameter params(project,fields);


params(project,'capacity_cost')=12;


set demand_period /d1,d2,d3/;
set energy_period /e1,e2,e3/;

set month /m1*m12/;
set hour /h1*h24/;
set day_of_week /dow1*dow7/;

set weekend(day_of_week) /dow1,dow7/;
set weekday(day_of_week) /dow2*dow6/;

set demand_weekday_schedule(site,month,hour,demand_period);
set demand_weekend_schedule(site,month,hour,demand_period);

set energy_weekday_schedule(site,month,hour,energy_period)  /
	site_a.m1.h1.d1
	site_a.m1.h2.d1
/;
set energy_weekend_schedule(site,month,hour,energy_period);

energy_weekend_schedule('site_a','m1','h1','d1')=YES;

