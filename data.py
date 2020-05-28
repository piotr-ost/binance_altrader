import pandas as pd
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.average_true_range import average_true_range as atr
from pyti.money_flow_index import money_flow_index as mfi

class SpotData:
	def __init__(self,client,symbol,interval):
		self.client = client
		self.symbol = symbol
		self.interval = interval

	def get_data(self):
		data = self.client.get_klines(
			symbol=self.symbol,
			interval=self.interval,
			limit=200)
		df = pd.DataFrame(data,columns=[
			'open time',
			'open',
			'high',
			'low',
			'close',
			'volume',
			'close time',
			'quote asset volume',
			'number of trades',
			'_','_','_'])
		df.set_index('open time',inplace=True)
		df = df[['open','high','low','close','volume']]
		#df = pd.to_numeric(df)
		df.index = pd.to_datetime(df.index, unit='ms')
		return df

	def get_rsi(self):
		df = self.get_data()
		df['RSI'] = rsi(df['close'],14)
		RSI = df['RSI']
		return RSI

	def get_ma(self,period):
		df = self.get_data()
		df['MA'] = sma(df['close'],period)
		MA = df['MA']
		return MA
	
	def get_atr(self):
		df = self.get_data()
		df['ATR'] = atr(df['close'],14)
		ATR = df['ATR']
		return ATR
	
	def get_mfi(self):
		df = self.get_data()
		df['MFI'] = mfi(
    		close_data=df['close'],
    		high_data=df['high'],
    		low_data=df['low'],
    		volume=df['volume'],
    		period=14)
		MFI = df['MFI']
		return MFI 

from client import client
#print(SpotData(client,'ETHUSDT','5m').get_mfi())
print(SpotData(client,'BTCUSDT','5m').get_data()['volume'][-1])

#choose the best oscillator
#figure a strategy for buying altcoins
#and many many more things lol
