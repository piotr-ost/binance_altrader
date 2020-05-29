#define an orderqty adjuster to altcoins that notices the pairing in some way and converts usd order into an amount of this given altcoin

#get all the currently trading symbols

#stop loss and tp adjuster using ATR

#main strategy that goes through all the symbols in a loop, sleep for 1 min and continue depending on timeframe

###main strat
'''if alt volume spikes and alt between +0-5% for the day and alt not in usdt pairing, buy
possibly reach out to someone with alt trading experience and ask for a short interview?''' 	

#an actually good strategy would be to buy mfi bounces whenever altcoin price > weekly open, that is what
from spot import SpotTrade
from data import SpotData
from client import client
from cross_overs import CrossesOver,CrossesUnder

class Main:
	def __init__(self,symbol,interval,client=client):
		self.trade = SpotTrade(client,symbol)
		self.data = SpotData(client,symbol,interval)
		#self.quantity = 
	
	def mfi_swing(self):
		if self.data.last_price() > self.data.weekly_open():
			if self.trade.