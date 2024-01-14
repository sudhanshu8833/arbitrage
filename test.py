from pprint import pprint
from binance.client import Client
import math
# api_key = '8lDeuoPStUdNJSmQDgxxvCVtwbM2urIOJV5JTC7rHLjUoDiTjdGWx3OSKLxa9tpM'
# api_secret = '5GjP04VXQuJ2mhai3NrNdU1YhyCpVCH100qzZhLZXBcsKzJPTNfjuelDJQgMHUT6'
api_key = 'GUf7tyd95mZMW7xXhKSuXXUhvenGaFZURNrrYFmecqZfFKGuzmYO9dRoPPR1xHTh'
api_secret = 'FGTiA20a37iEQzTgpv8pQnI4QIeNVlx6EEq5Dfu5rHB60tZVHNB1US8bc4Zu4atw'


client = Client(api_key, api_secret)
# exchange.set_sandbox_mode(True)
# data=client.get_all_tickers()
data=client.get_orderbook_tickers()

pprint(data)
# def round_down(value, decimal_places):
#     multiplier = 10 ** decimal_places
#     return int(value * multiplier) / multiplier

# def get_balance(client,base):
#     account_info = client.get_account()
#     for wallet in account_info['balances']:
#         if wallet["asset"]==base:
#             return float(wallet['free'])
#     return 1



# val=5
# while(val):
#     val-=1

BALANCE=get_balance(client,"USDT")
print(BALANCE)
order_response = client.create_order(symbol='BTCUSDT',
                                        side='BUY',
                                        type='MARKET',
                                        quoteOrderQty=30
                                        )
    
print(order_response)

print(get_balance(client,"USDT"))
# dicti={'symbol': 'STXUSDT', 'orderId': 702934853, 'orderListId': -1, 'clientOrderId': 'R8L3YQUtQvapUd82dlafkQ', 'transactTime': 1704107819106, 'price': '0.00000000', 'origQty': '20.10000000', 'executedQty': '20.10000000', 'cummulativeQuoteQty': '29.92488000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'workingTime': 1704107819106, 'fills': [{'price': '1.48880000', 'qty': '20.10000000', 'commission': '0.02010000', 'commissionAsset': 'STX', 'tradeId': 50178333}], 'selfTradePreventionMode': 'EXPIRE_MAKER'}
# pprint(dicti)

