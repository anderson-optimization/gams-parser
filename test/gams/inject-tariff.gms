set product /energy,demand/;
set period /period1*period10/;
set tier /tier1*tier10/;

set weekday_schedule(supply,product,month,hour,period);
set weekend_schedule(supply,product,month,hour,period);

parameter product_rate(supply,product,period,tier);

** Schedule definition

set weekend_schedule /
	supply1.energy.m1.h1.period1
	supply1.energy.m1.h2.period1
	supply1.energy.m1.h3.period1
/;


parameter product_rate /
	supply1.energy.period1.tier1 10.4
	supply1.energy.period1.tier2 15.2
/;
