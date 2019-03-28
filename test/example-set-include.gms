set bus_sub_network(bus,sub_network)  "load to bus map" /
$include %mapfolder%bus_sub_network.csv
/;

set load_bus(load,bus)  "load to bus map" /
$include %mapfolder%load_bus.csv
/;
set gen_bus(gen,bus)  "gen to bus map" /
$include %mapfolder%gen_bus.csv
/;
set branch_bus0(branch,bus)  "branch to bus0 map" /
$include %mapfolder%branch_bus0.csv
/;
set branch_bus1(branch,bus)  "branch to bus1 map" /
$include %mapfolder%branch_bus1.csv
/;


set gen_energy_source(gen,energy_source) /
$include %mapfolder%gen_energy_source.csv
/;
set gen_startup_source(gen,energy_source)   /
$include %mapfolder%gen_startup_source.csv
/;
set gen_prime_mover(gen,prime_mover)  /
$include %mapfolder%gen_prime_mover.csv
/;
set gen_technology(gen,technology)   /
$include %mapfolder%gen_technology.csv
/;

set eia_plant_eia_gen(eia_plant,eia_gen)   /
$include %mapfolder%eia_plant_eia_gen.csv
/;
set gen_eia_plant(gen,eia_plant)  /
$include %mapfolder%gen_eia_plant.csv
/;
set gen_eia_gen(gen,eia_gen)   /
$include %mapfolder%gen_eia_gen.csv
/;
