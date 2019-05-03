
* Data sets , probably a csv
table demand(time,site)
$offlisting
	SiteA_Parcel
**ao json2data group=demand "t{_index}	{row.AverageLoad(kW)}"
$onlisting
;
