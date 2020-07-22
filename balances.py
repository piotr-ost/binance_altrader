import webbrowser

from util.client import client


def get_balances():
    pool = [x['symbol'] for x in client.get_all_tickers()
            if x['symbol'][-3:] == 'BTC']

    data = client.get_account()
    assets = [d['asset'] for d in data['balances']
              if float(d['free']) != 0 or float(d['locked']) != 0]

    balances = [client.get_asset_balance(asset)['free'] for asset in assets]
    return zip(assets, balances)


if __name__ == '__main__':
    print(f"Balances: ")
    for i in get_balances():
        print(f'{i[0]}: {i[1]}')
    print('Show charts? (y/n)')
    if input() == 'y':
        for asset in assets:
            webbrowser.open(
                f'https://www.binance.com/en/trade/pro/{asset}_BTC')
            print(f'https://www.binance.com/en/trade/pro/{asset}_BTC')
