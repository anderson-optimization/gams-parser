
* Data sets , probably a csv
table p_max_pu_t(time,gen) 
$offlisting
	new_solar
**ao json2data nrel-sam-gen "t{_index}	{row.gen}"
$onlisting
;

