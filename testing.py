# from pprint import pprint
# from binance.client import Client
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri, server_api=ServerApi('1'))
# bot = client['bot']
# admin = bot['admin']


# symbols=['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH', 'GASBTC', 'BNBETH', 'BTCUSDT', 'ETHUSDT', 'LRCBTC', 'LRCETH', 'QTUMBTC', 'ZRXBTC', 'KNCBTC', 'FUNETH', 'NEOETH', 'IOTABTC', 'IOTAETH', 'LINKBTC', 'LINKETH', 'XVGETH', 'MTLBTC', 'EOSBTC', 'SNTBTC', 'ETCETH', 'ETCBTC', 'ZECBTC', 'ZECETH', 'BNTBTC', 'ASTBTC', 'DASHBTC', 'DASHETH', 'OAXBTC', 'REQBTC', 'VIBBTC', 'TRXBTC', 'TRXETH', 'POWRBTC', 'POWRETH', 'XRPBTC', 'XRPETH', 'ENJBTC', 'ENJETH', 'STORJBTC', 'BNBUSDT', 'KMDBTC', 'NULSBTC', 'XMRBTC', 'XMRETH', 'AMBBTC', 'BATBTC', 'NEOUSDT', 'LSKBTC', 'LSKETH', 'MANABTC', 'MANAETH', 'ADXBTC', 'ADXETH', 'ADABTC', 'ADAETH', 'XLMBTC', 'XLMETH', 'XLMBNB', 'LTCETH', 'LTCUSDT', 'LTCBNB', 'WAVESBTC', 'WAVESETH', 'ICXBTC', 'ELFBTC', 'ELFETH', 'RLCBTC', 'RLCETH', 'PIVXBTC', 'IOSTBTC', 'IOSTETH', 'STEEMBTC', 'STEEMETH', 'BLZBTC', 'ZILBTC', 'ZILETH', 'ONTBTC', 'QTUMUSDT', 'WANBTC', 'WANETH', 'SYSBTC', 'ADAUSDT', 'ADABNB', 'LOOMBTC', 'XRPUSDT', 'BTCTUSD', 'ETHTUSD']
# data=admin.find_one()
# data['symbols']=symbols

# admin.update_one({},{"$set":data})
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

# Replace YOUR_API_KEY and YOUR_API_SECRET with your actual Binance API key and secret
# api_key = 'GUf7tyd95mZMW7xXhKSuXXUhvenGaFZURNrrYFmecqZfFKGuzmYO9dRoPPR1xHTh'
# api_secret = 'FGTiA20a37iEQzTgpv8pQnI4QIeNVlx6EEq5Dfu5rHB60tZVHNB1US8bc4Zu4atw'

# client = Client(api_key, api_secret)

# # Get account information
# data = client.get_all_tickers()
# # print(data)
# exchange_info = client.get_exchange_info()

# delisted_coins = []
# for symbol_info in exchange_info['symbols']:
#     if symbol_info['status'] != 'TRADING':
#         delisted_coins.append(symbol_info['symbol'])


# # print(delisted_coins)

# symbols=[]

# for sym in data:
#     if sym['symbol'] not in delisted_coins:
#         symbols.append(sym['symbol'])
# print(symbols)