from spot import SpotTrade
from client import client

class SellAll(SpotTrade):

    '''tool to get rid of all assets in case of emergency
    '''

    def __init__(self):
        #specyfing the symbol is not required
        SpotTrade.__init__(self,symbol='',client=client)


    def assets(self):
        data = client.get_account()
        assets = [d['asset'] for d in data['balances'] if float(d['free']) != 0 or float(d['locked']) != 0]
        balances = [client.get_asset_balance(asset)['free'] for asset in assets]
        for asset,balance in list(zip(assets,balances)):
            if asset != 'BNB' and asset != 'BTC':
                self.symbol = asset + 'BTC'
                self.market_order_sell(balance)
        print('Sell btc for usdt too? (y/n) Damn market must be going crazy')
        if input() == 'y':
            self.symbol = 'BTCUSDT'
            self.market_order_sell(self.converter(self.asset_free_balance('BTC')*self.last_price()))
        print(f'All tethered, only some BNB left: {self.asset_free_balance("BNB")}')

#TODO:
# File "/home/piotr/Projects/binance_v1/spot.py", line 96, in converter
# quantity = quantity / self.last_price()
# TypeError: unsupported operand type(s) for /: 'str' and 'float',
# Im bullish on btc and gfms project is main focus, gon fix it l8


if __name__ == '__main__':
    SellAll().assets()

