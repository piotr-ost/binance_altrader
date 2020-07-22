import pandas as pd


class SpotData:
    def __init__(self, client, symbol, interval):
        self.client = client
        self.symbol = symbol
        self.interval = interval

    def get_data(self):
        data = self.client.get_klines(
            symbol=self.symbol,
            interval=self.interval,
            limit=200)

        df = pd.DataFrame(data, columns=[
            'open time',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close time',
            'quote asset volume',
            'number of trades',
            '_', '_', '_'])
        df.set_index('open time', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume',
                 'quote asset volume']]
        df = df.apply(pd.to_numeric)
        df.index = pd.to_datetime(df.index, unit='ms')
        return df

    def btc_price(self):
        btc_price = SpotData(self.client, 'BTCUSDT', '_').last_price()
        return btc_price

    def last_price(self):
        last_price = float(self.client.get_symbol_ticker(
            symbol=self.symbol)['price'])
        return last_price

    def weekly_open(self):
        df = SpotData(self.client, self.symbol, '1w').get_data()
        weekly_open = df['open'][-1]
        return weekly_open

    def daily_open(self):
        df = SpotData(self.client, self.symbol, '1d').get_data()
        daily_open = df['open'][-1]
        return daily_open
