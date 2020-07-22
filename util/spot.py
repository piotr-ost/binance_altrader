from datetime import datetime


def current_time():
	return datetime.now().strftime("%H:%M:%S")


class SpotTrade:
	""" Note:
		1) minimum order size is 10 usd
		2) quantities have to be in BTC
	"""

	def __init__(self, client, symbol):
		self.client = client
		self.symbol = symbol

	def market_order_buy(self, quantity):
		try:
			self.client.order_market_buy(
				symbol=self.symbol,
				quantity=quantity)
			print(f'Bought.\
				\nSymbol: {self.symbol}\
				\nPrice: {self.last_price()}\
				\nQuantity: {quantity}\
				\nTime: {current_time()}')
		except Exception as e:
			print(e)

	def market_order_sell(self, quantity):
		try:
			self.client.order_market_sell(
				symbol=self.symbol,
				quantity=quantity)
			print(f'Sold.\
				\nSymbol: {self.symbol}\
				\nPrice: {self.last_price()}\
				\nQuantity: {quantity}\
				\nTime: {current_time()}')
		except Exception as e:
			print(e)

	def oco_sell(self, price, stop_price, quantity):
		"""oco can only be placed when already in position"""
		try:
			self.client.order_oco_sell(
				symbol=self.symbol,
				quantity=quantity,
				price=price,
				stopPrice=stop_price,
				stopLimitPrice=stop_price,
				stopLimitTimeInForce='GTC')
			print(
				f'OCO has been submitted.\
				\nSymbol: {self.symbol}\
				\nTake Profit: {price}\
				\nStop Loss: {stop_price}\
				\nQuantity: {quantity}\
				\nTime: {current_time()}')
		except Exception as e:
			print(e)

	def limit_sell(self, price, quantity):
		try:
			self.client.order_limit(
				symbol=self.symbol,
				side='sell',
				quantity=quantity,
				price=price)
			print(
				f'Limit sell has been submitted.\
				\nSymbol: {self.symbol}\
				\nPrice: {price}\
				\nQuantity: {quantity}\
				\nTime: {current_time()}')
		except Exception as e:
			print(e)

	def last_price(self):
		last_price = float(self.client.get_symbol_ticker(
			symbol=self.symbol)['price'])
		return last_price

	def converter(self, quantity):
		"""
		the precision value varies depending on symbol
		it tends to : higher price <==> more decimal points
		"""
		min_qty = self.client.get_symbol_info(
			self.symbol)['filters'][2]['minQty']
		precision = min_qty.split('.')[1].find('1') + 1
		if self.symbol.endswith('BTC'):
			quantity = self.to_btc(quantity) / self.last_price()
		if self.symbol.endswith('USDT'):
			quantity = quantity / self.last_price()
		return round(quantity, precision)

	def asset_locked_balance(self):
		symbol = self.symbol
		if symbol[-3:] == 'BTC':
			return self.client.get_asset_balance(symbol[:-3])['locked']
		if symbol[-4:] == 'USDT':
			return self.client.get_asset_balance(symbol[-4:])['locked']

	def asset_free_balance(self, asset):
		if asset is not None:
			current_qty = self.client.get_asset_balance(asset)['free']
			return current_qty

		else:
			symbol = self.symbol
			if symbol.endswith('BTC'):
				asset = symbol[:-3]
			if symbol.endswith('USDT'):
				asset = symbol[:-4]
			current_qty = self.client.get_asset_balance(asset)['free']
			return current_qty
