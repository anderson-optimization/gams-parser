
storage_balance(battery,time)$ch(time)..

	energyX(battery,time+1) =e=
		energyX(battery,time)
		+ storeX(battery,time)*efficiency_store(battery)
		- dispatchX(battery,time);
