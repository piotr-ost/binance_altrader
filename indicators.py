from data import SpotData 
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.average_true_range import average_true_range as atr
from pyti.money_flow_index import money_flow_index as mfi

class Indicators(SpotData):

	def __init__(self,client,symbol,interval):
		self.client = client
		self.symbol = symbol
		self.interval = interval

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