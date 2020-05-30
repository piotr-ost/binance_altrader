from spot import SpotTrade
from data import SpotData
from client import client
from cross_overs import CrossesOver,CrossesUnder
from indicators import Indicators

class Main:

#get all the currently trading symbols

#stop loss and tp adjuster using ATR

#main strategy that goes through all the symbols in a loop, sleep for 1 min and continue depending on timeframe

#if btc in uptrend - trade btc pairings, hold btc
#if btc is falling - trade usdt pairings, hold tether

###main strat
	'''if alt volume spikes and alt between +0-5% for the day and alt not in usdt pairing, buy
	possibly reach out to someone with alt trading experience and ask for a short interview?''' 	

#an actually good strategy would be to buy mfi bounces whenever altcoin price > weekly open

	client=client

	def __init__(self,symbol,interval):
		self.symbol = symbol
		self.trade = SpotTrade(client,symbol)
		self.data = SpotData(client,symbol,interval)
		self.indicators = Indicators(client,symbol,interval)
	
	def converter(self,quantity):
		'''
		the precision value varies depending on symbol
		it tends to : higher price <==> more decimal points
		fix asap and deploy strat, errting else work
		'''
		precision = ''
		if self.symbol[-3:] == 'BTC':
			quantity = self.to_btc(quantity)/self.data.last_price()
		if self.symbol[-4:] == 'USDT':
			quantity = quantity/self.data.last_price()
		return round(quantity,precision)


	def to_btc(self,quantity):
		return quantity/self.data.btc_price()

	
	# def mfi_swing(self,quantity):
	# 	if self.data.last_price() > self.data.weekly_open():
	# 		if self.trade.asset_balance():
	#			pass

m = Main('ETHUSDT','5m')