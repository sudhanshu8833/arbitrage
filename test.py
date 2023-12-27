from pprint import pprint
from binance.client import Client
api_key = '8lDeuoPStUdNJSmQDgxxvCVtwbM2urIOJV5JTC7rHLjUoDiTjdGWx3OSKLxa9tpM'
api_secret = '5GjP04VXQuJ2mhai3NrNdU1YhyCpVCH100qzZhLZXBcsKzJPTNfjuelDJQgMHUT6'
client = Client(api_key, api_secret)

# symbols=[sym['symbol'] for sym in (client.get_all_tickers())]

# print(symbols)

def get_balance(client,base):
    account_info = client.get_account()
    for wallet in account_info['balances']:
        if wallet["asset"]==base:
            return float(wallet['free'])

    return 1

# order_response = client.create_order(symbol='GBPUSDT',
#                                      side='SELL',
#                                      type='MARKET',
#                                      quantity=17.3)

# print(order_response)
print(get_balance(client,"USDT"))