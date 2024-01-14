from binance.client import Client
from binance.enums import *
from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import os
import sys
import logging
import requests
import sys

database='arbitrage'

script_dir = os.path.dirname(os.path.realpath(__file__))
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
# Create the 'log' directory if it doesn't exist
log_dir = os.path.join(script_dir, 'log')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=log_dir+'/dev.log',
    level=logging.DEBUG,  # You can adjust the log level as needed
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get and print the public IP address

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("pymongo").setLevel(logging.WARNING)
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client1 = MongoClient(uri, server_api=ServerApi('1'),connect=False)
bot=client1[database]
admin=bot['admin']

logins={}

script_dir = os.path.dirname(os.path.realpath(__file__))
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)

precision={}
with open(script_dir+"/prec.json",'r') as json_file:
    precision=json.load(json_file)




def round_down(value, decimal_places):
    multiplier = 10 ** decimal_places
    return int(value * multiplier) / multiplier


def login(api_key,secret_key):
    if api_key in logins:
        return logins[api_key]
    
    client = Client(api_key, secret_key)
    logins[api_key]=client

    return client

def get_balance(client,base):
    account_info = client.get_account()
    for wallet in account_info['balances']:
        if wallet["asset"]==base:
            return float(wallet['free'])

    
    return 0

def ltp_price(client):
    prices = client.get_orderbook_tickers()
    price_dict={}


    for price in prices:
        temp={}
        temp['bid']=price['bidPrice']
        temp['ask']=price['askPrice']
        price_dict[price['symbol']]=temp

    return price_dict

def market_order(client,instrument,side,type,quantity):

    dici={
        'int':instrument,
        'side':side,
        'type':type,
        'quan':quantity
    }
    logger.info(dici)
    order_response="no_order"
    if(side=="BUY"):

        order_response=client.create_order(symbol=instrument,
                                        side=side,
                                        type=type,
                                        quoteOrderQty=quantity)


    if(side=="SELL"):
        order_response=client.create_order(symbol=instrument,
                                        side=side,
                                        type=type,
                                        quantity=round_down(quantity,precision[instrument]["round"]))

    logger.info(order_response)

    return order_response


if __name__=="__main__":
    c=login("GUf7tyd95mZMW7xXhKSuXXUhvenGaFZURNrrYFmecqZfFKGuzmYO9dRoPPR1xHTh","FGTiA20a37iEQzTgpv8pQnI4QIeNVlx6EEq5Dfu5rHB60tZVHNB1US8bc4Zu4atw")
    ltp_price(c)



