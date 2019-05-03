import os
import logging
import csv
logger = logging.getLogger('gams_writer')


class GamsWriter():
	def __init__(self,dump_folder):
		if not dump_folder:
			raise ValueError('Need a dump folder for GamsWriter')
		self.dump_folder=dump_folder

	def dump_set(self,name,df):
		path="{}/{}.csv".format(self.dump_folder,name)
		folder=os.path.dirname(path)
		if not os.path.exists(folder):
		    os.makedirs(folder)
		try:
			df.to_csv(path,columns=[],header=False)
			logger.debug('DumpSet:{}, items:{}'.format(name,len(df)))
			return
		except AttributeError as e:
			logger.debug('Not a dataframe, try list')

		with open(path,'w') as out_file:
			out_writer = csv.writer(out_file, delimiter=' ',
										quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for item in df:
				out_writer.writerow([item])


	def dump_param(self,name,df,sep=",",ignore_zero=False,round_decimals=None,key=None,header=False):
		if key:
			try:
				df = df[key]
			except KeyError as e:
				logger.warning('Error dumping dataset {}, no key {}'.format(name,e))
				df = pd.DataFrame()
		if round_decimals:
			df=df.round(round_decimals)
		path="{}/{}.csv".format(self.dump_folder,name)
		folder=os.path.dirname(path)
		if not os.path.exists(folder):
		    os.makedirs(folder)
		if ignore_zero:
			logger.debug('Ignore zeros')
			df=df[df.notna()]
		df.to_csv(path,header=header,sep=sep)
		logger.debug('DumpParam:{}, items:{}'.format(name,len(df)))

	def dump_param_t(self,name,df,sep=",",ignore_zero=False,round_decimals=None,key=None):
		if key:
			try:
				df = df[key]
			except KeyError as e:
				logger.warning('Error dumping dataset {}, no key {}'.format(name,e))
				df = pd.DataFrame()
		if round_decimals:
			df=df.round(round_decimals)
		path="{}/{}.csv".format(self.dump_folder,name)
		folder=os.path.dirname(path)
		if not os.path.exists(folder):
		    os.makedirs(folder)
		if ignore_zero:
			logger.debug('Ignore zeros')
			df=df[df.notna()]
		df.to_csv(path,sep=sep)
		logger.debug('DumpParam:{}, items:{}'.format(name,len(df)))