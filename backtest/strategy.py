import binance_api
import traceback
import math
import pandas as pd

from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from blog import *
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
    # print(prices)
    symbols=[]
    base_currency=[]
    with open("backtest/tokens.json",'r') as json_file:
        symbols=json.load(json_file)['symbols']
        # base_currency=json.load(json_file)['base']

    
    combinations=get_crypto_combinations(symbols,data['tradable_base_coins'])
    # print(pd.DataFrame(combinations))

    results=[]
    for comb in combinations:
        base = comb['base']
        intermediate = comb['intermediate']
        ticker = comb['ticker']
        
        s1 = f'{intermediate}{base}'    # Eg: BTC/USDT
        s2 = f'{ticker}{intermediate}'  # Eg: ETH/BTC
        s3 = f'{ticker}{base}'          # Eg: ETH/USDT 

        final_price1,scrip_price1 = check_buy_buy_sell(s1,s2,s3,data['investment'],prices)
        profit_loss1 = check_profit_loss(final_price1,data['investment'], data['bank_fees'], data['minimum_profit'])

        if profit_loss1>0:
            # place_trade_orders(client,"BUY_BUY_SELL",s1,s2,s3,data['investment'],scrip_price1)
            result=[base,s1,prices[s1],s2,prices[s2],s3,prices[s3],100,final_price1,"BUY_BUY_SELL"]
            results.append(result)
            # print(str(s1)+" "+s2+" "+s3+" "+str(data['investment'])+' '+str(final_price1)+" BUY_BUY_SELL")

        final_price2,scrip_price2 = check_buy_sell_sell(s3,s2,s1,data['investment'],prices)
        profit_loss2 = check_profit_loss(final_price2,data['investment'], data['bank_fees'], data['minimum_profit'])

        if profit_loss2>0:
            # place_trade_orders(client,"BUY_BUY_SELL",s1,s2,s3,data['investment'],scrip_price1)
            # print(s1+" "+s2+" "+s3+" "+str(data['investment'])+' '+str(final_price2)+" BUY_SELL_SELL")
            result=[base,s3,prices[s3],s2,prices[s2],s1,prices[s1],100,final_price2,"BUY_SELL_SELL"]
            results.append(result)

    df=pd.DataFrame(results,columns=['base','script1', 'script_price1', 'script2','script_price2','script3','script_price3','initial base quantity','final base quantity','arbitrage type'])
    print(df)
    df.to_csv('results.csv')

def run():
    while True:

        try:
            main()
        except Exception:
            if str(traceback.format_exc()) not in errors:
                logger.info(str(traceback.format_exc()))
                errors.append(str(traceback.format_exc()))


if __name__=="__main__":
    main()
    