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
		df = df[['open','high','low','close','volume','quote asset volume']]
		df = df.apply(pd.to_numeric)
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
		#this compared to tradingview isnt perfect, but more less like it, other ind work fine
		df = self.get_data()
		df['MFI'] = mfi(
    		close_data=df['close'],
    		high_data=df['high'],
    		low_data=df['low'],
    		volume=df['volume'],
    		period=14)
		MFI = df['MFI']
		return MFI 

	def last_price(self):
		last_price=round(float(self.client.get_symbol_ticker(
			symbol=self.symbol)['price']),2)
		return last_price

	def weekly_open(self): 
		df = SpotData(self.client,self.symbol,'1w').get_data()
		weekly_open = df['open'][-1]
		return weekly_open