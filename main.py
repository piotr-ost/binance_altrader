from spot import SpotTrade
from data import SpotData
from client import client
from cross_overs import CrossesOver,CrossesUnder
from indicators import Indicators
import time
import webbrowser

class Main:

	'''
	if btc in uptrend - trade btc pairings, hold btc
	if btc is falling - trade usdt pairings, hold tether
	fix:
	1) APIError(code=-1111): Precision is over the maximum defined for this asset.
	Symbol: LTCBTC
	Price: 0.004909
	Quantity: 0.21
	Time: 18:00:35
	2) APIError(code=-1013): Stop loss orders are not supported for this symbol.
	add:
	consider fibonacci an awesome strategy, peaks from codewars
	rest api forex try to connect using technique from video spotify
	add volume param and whenever volume is significantly higher on 1 min -
	trigger a buy signal
	(lets say average of the day for the given interval
	'''

	client=client

	def __init__(self,symbol,interval):
		self.symbol = symbol
		self.trade = SpotTrade(client,symbol)
		self.data = SpotData(client,symbol,interval)
		self.indicators = Indicators(client,symbol,interval)
		self.ignored = []
	
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

	
	def altcoin_scanner(self,quantity):
		'''
		NOTE! using weekly open and daily open to point trend is only good for very short timeframes,
		a better way for most timeframes would be to use weekly open and some other trend tool,
		for example a moving average, continue research
		'''
		last_price = self.data.last_price()
		weekly_open = self.data.weekly_open()
		daily_open = self.data.daily_open()
		if last_price > weekly_open and symbol not in self.ignored:
			MFI = round(self.indicators.get_mfi(),2)
			print(f'Symbol: {self.symbol},\
			 \nLatest MFI vals: {MFI[-2]}, {MFI[-1]}\
			 \nDaily change: {round((1-last_price/daily_open)*100,2)}%\
			 \n------------')
			if CrossesOver(MFI,20):
				ATR = Indicators(client,self.symbol,'4h').get_atr()
				take_profit = last_price + 2*ATR
				stop_loss = last_price - ATR
				print(
					f'Buy signal!\
					\nEntry: {last_price}\
					\nTake Profit: {take_profit}\
					\nStop Loss: {stop_loss}\
					\nTime: {self.trade.current_time()}\
					\nShow chart? (y/n)'
				)
				if input() == 'y':
					#link assumes we are trading -btc pairs
					webbrowser.open(f'https://www.binance.com/en/trade/pro/{self.symbol[:-3]}_{self.symbol[-3:]}')

				print('Enter? (y/n)')
				if  input() == 'y':
					qty = self.converter(quantity)
					self.trade.market_order_buy(qty)
					self.trade.oco_sell(int(take_profit),int(stop_loss),qty)
					self.ignored.append(self.symbol)

if __name__=='__main__':
	while 1:
		pool = [x['symbol'] for x in client.get_all_tickers() if x['symbol'][-3:] == 'BTC']
		for symbol in pool:
			a = Main(symbol,'5m')
			a.altcoin_scanner(10)
		time.sleep(1)