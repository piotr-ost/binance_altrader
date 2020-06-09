'''
quick balances tool to use using terminal alias to monitor live performance
possible improvements could be ROE of every asset bought
'''
from client import client
import webbrowser

pool = [x['symbol'] for x in client.get_all_tickers() if x['symbol'][-3:] == 'BTC']

data = client.get_account()
assets = [d['asset'] for d in data['balances'] if float(d['free']) != 0 or float(d['locked']) != 0]

balances = [client.get_asset_balance(asset)['free'] for asset in assets]
l = zip(assets,balances)

if __name__=='__main__':
    print(f"Balances: ")
    for i in l:
        print(f'{i[0]}: {i[1]}')
    print('Show charts? (y/n)')
    if input() == 'y':
        for asset in assets:
            webbrowser.open(f'https://www.binance.com/en/trade/pro/{asset}_BTC')
            print(f'https://www.binance.com/en/trade/pro/{asset}_BTC')
