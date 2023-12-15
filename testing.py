from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
bot=client['arbitrage']
admin=bot['admin']

d={
    "api_key":"GUf7tyd95mZMW7xXhKSuXXUhvenGaFZURNrrYFmecqZfFKGuzmYO9dRoPPR1xHTh",
    "secret_key":"FGTiA20a37iEQzTgpv8pQnI4QIeNVlx6EEq5Dfu5rHB60tZVHNB1US8bc4Zu4atw",
    "bank_fees":.01,
    "exchange":"BINANCE",
    "tradable_base_coins":["BTC","USDT","ETH"],
    "blacklist_pairs":["BTCUSDT","ETHUSDT"],
    "paper_trading":True,
    "investment":500,
    "minimum_profit":1.50,
    "stoploss":200
}
admin.insert_one(d)