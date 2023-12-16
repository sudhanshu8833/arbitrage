from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
bot=client['arbitrage']
admin=bot['admin']
trades=bot['trades']
# trades.delete_many({})

# # d={
# #     "api_key":"GUf7tyd95mZMW7xXhKSuXXUhvenGaFZURNrrYFmecqZfFKGuzmYO9dRoPPR1xHTh",
# #     "secret_key":"FGTiA20a37iEQzTgpv8pQnI4QIeNVlx6EEq5Dfu5rHB60tZVHNB1US8bc4Zu4atw",
# #     "bank_fees":.01,
# #     "exchange":"BINANCE",
# #     "tradable_base_coins":["BTC","USDT","ETH"],
# #     "blacklist_pairs":["BTCUSDT","ETHUSDT"],
# #     "paper_trading":True,
# #     "investment":500,
# #     "minimum_profit":1.50,
# #     "stoploss":200
# # }

# d={
#     "symbol1":"BTCUSDT",
#     "price1":19000,
#     "symbol2":"ETHBTC",
#     "price2":1,
#     "symbol3":"ETHUSDT",
#     "price3":2000,
#     "type":"BUY_BUY_SELL",
#     "investment":500,
#     "net_profits":2,
    
# }
# trades.insert_one(d)
from binance.client import Client
from pprint import pprint

# Replace YOUR_API_KEY and YOUR_API_SECRET with your actual Binance API key and secret
api_key = 'GUf7tyd95mZMW7xXhKSuXXUhvenGaFZURNrrYFmecqZfFKGuzmYO9dRoPPR1xHTh'
api_secret = 'FGTiA20a37iEQzTgpv8pQnI4QIeNVlx6EEq5Dfu5rHB60tZVHNB1US8bc4Zu4atw'

client = Client(api_key, api_secret)

# Get account information
account_info = client.get_account()
base="USDT"
balance=0
for wallet in account_info['balances']:
    if wallet["asset"]==base:
        balance=float(wallet['free'])
        break

pprint(balance)