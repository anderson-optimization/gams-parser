
set
*   Date time map
    datetime_comp         "Datetime components used to map a time index to a real datetime." 
                            /year,month,day,hour,minute,second/
    year                  "Years possible in the simulat" /y2018*y2028/
    month                 "Months of the year" /m1*m12/
    m2t(month,time)       "Map month to time";


Set       products  'Items produced' 
              / Chairs, Tables, Dressers /
          resources  'Resources limiting production'
              / RawWood, Labor, WarehouseSpace/
          hireterms  'Resource hiring terms'
              / Cost, Maxavailable /;


set weekend_schedule /
    supply1.energy.m1.h1.period1
    supply1.energy.m1.h2.period1
    supply1.energy.m1.h3.period1
/;
