import time
import webbrowser
from pyti.simple_moving_average import simple_moving_average as sma

from main import Main
from util.client import client


class Confluence(Main):
    """ Note:
    the bot is designed mainly for trading alt coins in btc parings,
    there are less USDT pairings and they tend to follow btc a lot
    """

    def __init__(self, symbol, interval):
        super().__init__(self, symbol, interval)

    def last_to_open(self, quantity):
        # using lesser timeframes filters out viable entries
        timeframes = ['5m', '15m', '30m', '1h', '4h', '1d']
        for timeframe in timeframes:
            self.data.interval = timeframe
            last_price = self.data.last_price()
            df = self.data.get_data()
            if last_price < df['open'][-1]:
                print(f'Bearish at {timeframe}.')
                return
            if last_price > df['open'][-1]:
                print(f'Bullish at {timeframe}')

        print(f'\
            \nConfluence of all timeframes on {self.symbol}!\
            \nShow chart? (y/n)')

        if input() == 'y':
            # under assumption we are trading -btc pairs
            webbrowser.open(
                f'https://www.binance.com/en/trade/pro/\
                {self.symbol[:-3]}_{self.symbol[-3:]}')

        last_price = self.data.last_price()
        # reverse the word to get instrument precision
        precision = str(last_price)[::-1].find('.')
        take_profit = round(last_price * 1.04, precision)
        stop_loss = round(last_price * 0.96, precision)

        print(f'\
            \nEntry: {self.data.last_price()} \
            \nTake Profit: {take_profit} \
            \nStop Loss: {stop_loss} \
            \nTime: {current_time()}\
            \nEnter? (y/n)')

        if input() == 'y':
            qty = self.converter(quantity)
            self.trade.market_order_buy(qty)
            self.trade.oco_sell(int(take_profit), int(stop_loss), qty)
            self.ignored.append(self.symbol)

    def last_to_ma(self, quantity, ma_period):
        # this method uses a few more timeframes, including short ones
        intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']
        for interval in intervals:
            self.data.interval = interval
            last_price = self.data.last_price()
            df = self.data.get_data()
            MA = sma(data=df['close'], period=ma_period)[-1]
            if last_price <= MA:
                print(f'{self.symbol} is bearish at {interval}.')
                return

        print(f'\
            \nConfluence of all timeframes on {self.symbol}!\
            \nShow chart? (y/n)')

        if input() == 'y':
            # under assumption we are trading -btc pairs
            base = 'https://www.binance.com/en/trade/pro/'
            webbrowser.open(
                f'{base}{self.symbol[:-3]}_{self.symbol[-3:]}')

        last_price = self.data.last_price()
        precision = str(last_price)[::-1].find('.')
        take_profit = round(last_price * 1.04, precision)
        stop_loss = round(last_price * 0.96, precision)
        
        print(f'\
            \nEntry: {self.data.last_price()} \
            \nTake Profit: {take_profit} \
            \nStop Loss: {stop_loss} \
            \nTime: {current_time()}\
            \nEnter? (y/n)')

        if input() == 'y':
            qty = self.converter(quantity)
            self.trade.market_order_buy(qty)
            self.trade.oco_sell(int(take_profit), int(stop_loss), qty - 1)
            self.ignored.append(self.symbol)


if __name__ == '__main__':
    while 1:
        pool = [x['symbol'] for x in client.get_all_tickers()
                if x['symbol'].endswith('BTC')]
        for symbol in pool:
            a = Confluence(symbol, '')
            a.last_to_ma(quantity=10, ma_period=50)
            time.sleep(1)
        time.sleep(5)
