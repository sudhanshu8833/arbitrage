from binance.client import Client
from binance.enums import *

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
bot=client['arbitrage']
admin=bot['admin']

logins={}

def login(api_key,secret_key):
    if api_key in logins:
        return logins[api_key]
    
    client = Client(api_key, secret_key)
    logins[api_key]=client
    return client


def ltp_price(client):
    prices = client.get_all_tickers()
    price_dict={}

    for price in prices:
        price_dict[price['symbol']]=price['price']

    return price_dict

def market_order(client,instrument,side,type,quantity):
    # order=client.create_order(symbol="BTCUSDT",
    #                     side="BUY",
    #                     type="MARKET",
    #                     quantity=.01
    #                     )

    data=admin.find_one()
    if data['paper_trading']==False:
        order_response=client.create_order(symbol=instrument,
                            side=side,
                            type=type,
                            quantity=quantity)
    
    return order_response
    

if __name__=="__main__":
    c=login("GUf7tyd95mZMW7xXhKSuXXUhvenGaFZURNrrYFmecqZfFKGuzmYO9dRoPPR1xHTh","FGTiA20a37iEQzTgpv8pQnI4QIeNVlx6EEq5Dfu5rHB60tZVHNB1US8bc4Zu4atw")
    ltp_price(c)



