from spot import SpotTrade
from data import SpotData
from client import client
from cross_overs import CrossesOver,CrossesUnder
from indicators import Indicators
import time

class Main:

	'''
	if btc in uptrend - trade btc pairings, hold btc
	if btc is falling - trade usdt pairings, hold tether
	'''

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
		'''
		min_qty = self.client.get_symbol_info(
			self.symbol)['filters'][2]['minQty']
		precision = min_qty.split('.')[1].find('1') + 1
		if self.symbol[-3:] == 'BTC':
			quantity = self.to_btc(quantity)/self.data.last_price()
		if self.symbol[-4:] == 'USDT':
			quantity = quantity/self.data.last_price()
		return round(quantity,precision) 


	def to_btc(self,quantity):
		return quantity/self.data.btc_price()

	
	def mfi_swing(self,quantity):
		#this one just buys when crosess 10 and sells when hits 80 
		#if self.trade.asset_locked_balance() == 0: #and available funds:
		last_price = self.data.last_price()
		weekly_open = self.data.weekly_open()
		#daily_open = self.data.daily_open()
		#for now lets try subtle trend filtering
		if last_price > weekly_open:
			MFI = self.indicators.get_mfi()
			print(f'symbol: {self.symbol}, last two MFI vals: {MFI[-2]}, {MFI[-1]}')
			if CrossesOver(MFI,20):
				ATR = Indicators(client,self.symbol,'4h').get_atr()
				take_profit = last_price + 2*ATR
				stop_loss = last_price + ATR
				# print(
				# 	f'Buy signal!\
				# 	\nEntry: {last_price}\
				# 	\nTake Profit: {take_profit}\
				# 	\nStop Loss: {stop_loss}\
				# 	\nTime: {self.trade.current_time()}')
				self.trade.market_order_buy(self.converter(quantity))
				self.trade.oco_sell(take_profit,stop_loss,self.converter(quantity))

if __name__=='__main__':
	#btc is in nice uptrend, so we trading btc pairs
	while 1:
		pool = [x['symbol'] for x in Main.client.get_all_tickers() if x['symbol'][-3:] == 'BTC']
		for symbol in pool:
			Main(symbol,'5m').mfi_swing(10)
	'''fix:
	1) APIError(code=-1100): Illegal characters found in parameter 'price'; legal range is '^([0-9]{1,20})([0-9]{1,20})?$'.
	2) APIError(code=-1111): Precision is over the maximum defined for this asset.
	Symbol: LTCBTC            
	Price: 0.004909            
	Quantity: 0.21            
	Time: 18:00:35'''
