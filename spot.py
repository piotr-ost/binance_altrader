from datetime import datetime

class SpotTrade:
	'''minimum order size is 10 usd'''
	def __init__(self,client,symbol):
		self.client = client
		self.symbol = symbol

	def market_order_buy(self,quantity):
		print(f'f"Buying...\
            \nSymbol: {self.symbol}\
            \nPrice: {self.last_price()}\
            \nQuantity: {quantity}\
            \nTime: {self.current_time()}')
		return self.client.order_market_buy(
				symbol=self.symbol,
				quantity=quantity)

	def oco_sell(self,price,stopPrice,quantity):
		'''oco can only be put when already in position'''
		print(f'f"Putting up an OCO...\
            \nSymbol: {self.symbol}\
            \nTake Profit: {price}\
            \nStop Loss: {stopPrice}\
            \nQuantity: {quantity}\
            \nTime: {self.current_time()}')
		return self.client.order_oco_sell(
			symbol=self.symbol,
			quantity=quantity,
			price=price,
			stopPrice=stopPrice)

	def last_price(self):
		last_price=round(float(self.client.get_symbol_ticker(
			symbol=self.symbol)['price']),2)
		return last_price
		 
	
	@staticmethod
	def current_time():
		current_time = datetime.now().strftime("%H:%M:%S")
		return current_time