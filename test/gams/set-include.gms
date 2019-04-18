set bus_sub_network(bus,sub_network)  "load to bus map" /
$include %mapfolder%bus_sub_network.csv
/;

set load_bus(load,bus)  "load to bus map" /
$include %mapfolder%load_bus.csv
/;
set gen_bus(gen,bus)  "gen to bus map" /
$include %mapfolder%gen_bus.csv
/;