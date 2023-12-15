import binance_api
import traceback

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
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
    prices=binance_api()

while True:

    try:
        main()
    except Exception:
        if str(traceback.format_exc()) not in errors:
            logger.info(str(traceback.format_exc()))
            errors.append(str(traceback.format_exc()))
    