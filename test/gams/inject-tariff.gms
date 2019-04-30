set product /energy,demand/;
set period /period1*period10/;
set tier /tier1*tier10/;

set weekday_schedule(supply,product,month,hour,period);
set weekend_schedule(supply,product,month,hour,period);

parameter product_rate(supply,product,period,tier);

** Schedule definition

parameter product_rate(supply,product,period,tier) /
supply1.energy.period1.tier1 10
supply1.demand.period1.tier1 10
/;

parameter product_rate(supply,product,period,tier) /
**ao tariff product_rate
/;
parameter product_adj(supply,product,period,tier) /
**ao tariff product_adj
/;

set weekend_schedule(supply,product,month,hour,period) /
	supply1.energy.m1.h1.period1
	supply1.energy.m1.h2.period1
	supply1.energy.m1.h3.period1
/;

set weekend_schedule(supply,product,month,hour,period) /
**ao tariff weekend_schedule
/;

set weekday_schedule(supply,product,month,hour,period) /
**ao tariff weekend_schedule
/;

