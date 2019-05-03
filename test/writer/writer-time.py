
from gams_parser import GamsWriter
import pandas as pd
import numpy as np

def test_write_datetime():
	gw = GamsWriter(dump_folder='tmp')
	year=2018
	time_map = pd.DataFrame(index=pd.date_range(str(year)+'-1-1', str(year+1)+'-1-1', freq="1h"))
	time_map['n']=np.arange(len(time_map))
	time_map['t']='t'+(time_map['n']).astype(str)
	time_map['date']=time_map.index
	time_map.index=time_map['t']
	gw.dump_set('set/time',time_map)

	time_map['year']=time_map['date'].dt.year
	time_map['month']=time_map['date'].dt.month
	time_map['day']=time_map['date'].dt.day
	time_map['hour']=time_map['date'].dt.hour
	time_map['minute']=time_map['date'].dt.minute
	time_map['dayofweek']=time_map['date'].dt.dayofweek
	
	# dayofweek 0=monday 6=sunday	
	time_map['weekday']=(time_map['date'].dt.dayofweek <5).astype(int)
	time_map['weekend']=(time_map['date'].dt.dayofweek >= 5).astype(int)
	print(time_map)

	datetime_cols=['year','month','day','hour','minute','weekend','weekday','dayofweek']
	gw.dump_param_t('time/datetime_map_{}'.format(year),time_map[datetime_cols])