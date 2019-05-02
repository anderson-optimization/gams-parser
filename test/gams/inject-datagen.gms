
* Data sets , probably a csv
table gen(time,gen) 
	new_solar
**ao json2data nrel-sam-gen "t{_index_p1}	{row.gen}"
;

