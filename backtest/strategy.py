import binance_api
import traceback
from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
bot=client['arbitrage']
admin=bot['admin']

import logging
logger = logging.getLogger('dev_log')
errors=[]

def main():
    data=admin.find_one()
    client=binance_api.login(data['api_key'],data['secret_key'])
    prices=binance_api.ltp_price(client)

    data=client.get_exchange_info()
    

    symbol_lists=[]
    symbols=data['symbols']
    for symbol in symbols:
        symbol_lists.append(symbol['baseAsset']+'/'+symbol['quoteAsset'])

    python_dict={"symbols":symbol_lists}

    with open("tokens.json","w") as json_file:
        json.dump(python_dict,json_file,indent=4)

# while True:

# try:
main()
# except Exception:
#     if str(traceback.format_exc()) not in errors:
#         logger.info(str(traceback.format_exc()))
#         errors.append(str(traceback.format_exc()))
    