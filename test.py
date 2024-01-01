from pprint import pprint
from binance.client import Client
import math
# api_key = '8lDeuoPStUdNJSmQDgxxvCVtwbM2urIOJV5JTC7rHLjUoDiTjdGWx3OSKLxa9tpM'
# api_secret = '5GjP04VXQuJ2mhai3NrNdU1YhyCpVCH100qzZhLZXBcsKzJPTNfjuelDJQgMHUT6'
api_key = 'GUf7tyd95mZMW7xXhKSuXXUhvenGaFZURNrrYFmecqZfFKGuzmYO9dRoPPR1xHTh'
api_secret = 'FGTiA20a37iEQzTgpv8pQnI4QIeNVlx6EEq5Dfu5rHB60tZVHNB1US8bc4Zu4atw'
client = Client(api_key, api_secret)

# symbols=[sym['symbol'] for sym in (client.get_all_tickers())]

# print(symbols)

def get_balance(client,base):
    account_info = client.get_account()
    for wallet in account_info['balances']:
        if wallet["asset"]==base:
            return float(wallet['free'])

    return 1

# order_response = client.create_order(symbol='ETHUSDT',
#                                      side='SELL',
#                                      type='MARKET',
#                                      quoteOrderQty=0.0381)

def round_down(value, decimal_places):
    multiplier = 10 ** decimal_places
    return int(value * multiplier) / multiplier

eth=get_balance(client,"LAZIO")
print(eth)
# order_response = client.create_order(symbol='ETHUSDT',
#                                      side='SELL',
#                                      type='MARKET',
#                                      quantity=round_down(eth,4))

# print(order_response)
