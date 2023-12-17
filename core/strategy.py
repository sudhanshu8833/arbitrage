import core.binance_api as binance_api
import traceback
import math
import pandas as pd
from datetime import datetime
from core.blog import *
import json
from pprint import pprint

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
bot=client['arbitrage']
admin=bot['admin']
trades=bot['trades']
screenshot=bot['screenshot']



logging.basicConfig(
    filename='log/dev.log',
    level=logging.DEBUG,  # You can adjust the log level as needed
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

errors=[]
delisted=[]

def find_delisted_coins():
    data=admin.find_one()
    client=binance_api.login(data['api_key'],data['secret_key'])
    exchange_info = client.get_exchange_info()

    delisted_coins = []
    for symbol_info in exchange_info['symbols']:
        if symbol_info['status'] != 'TRADING':
            delisted_coins.append(symbol_info['symbol'])
    
    return delisted_coins



def main():
    data=admin.find_one()
    client=binance_api.login(data['api_key'],data['secret_key'])
    prices=binance_api.ltp_price(client)

    symbols=[]
    base_currency=[]
    with open("core/tokens.json",'r') as json_file:
        symbols=json.load(json_file)['symbols']

    
    combinations=get_crypto_combinations(symbols,data['tradable_base_coins'])
    

    initial_balance=binance_api.get_balance(client,data['tradable_base_coins'])

    results=[]
    for comb in combinations:
        base = comb['base']
        intermediate = comb['intermediate']
        ticker = comb['ticker']
        
        s1 = f'{intermediate}{base}'    # Eg: BTC/USDT
        s2 = f'{ticker}{intermediate}'  # Eg: ETH/BTC
        s3 = f'{ticker}{base}'          # Eg: ETH/USDT 

        if s1 in delisted or s2 in delisted or s3 in delisted:
            continue
        final_price1,scrip_price1 = check_buy_buy_sell(s1,s2,s3,float(data['investment']),prices)
        profit_loss1,final_price1 = check_profit_loss(final_price1,float(data['investment']), data['bank_fees'], float(data['minimum_profit']))

        if profit_loss1>=float(data['minimum_profit']):
            result=[datetime.now(),base,s1,prices[s1],s2,prices[s2],s3,prices[s3],float(data['investment']),final_price1,profit_loss1,"BUY_BUY_SELL"]
            results.append(result)


        final_price2,scrip_price2 = check_buy_sell_sell(s3,s2,s1,float(float(data['investment'])),prices)
        profit_loss2,final_price2 = check_profit_loss(final_price2,float(data['investment']), data['bank_fees'], float(data['minimum_profit']))

        if profit_loss2>=float(data['minimum_profit']):
            result=[datetime.now(),base,s3,prices[s3],s2,prices[s2],s1,prices[s1],float(data['investment']),final_price2,profit_loss2,"BUY_SELL_SELL"]
            results.append(result)

    df=pd.DataFrame(results,columns=["time",'base','script1', 'script_price1', 'script2','script_price2','script3','script_price3','initial base quantity','final base quantity','profit','arbitrage type'])
    df=df.sort_values(by='final base quantity', ascending=False)

    if df['profit'].iloc[0]>=float(data['minimum_profit']):

        if data['paper_trading']==False:
            try:
                place_trade_orders(client,df["arbitrage type"].iloc[0],df['script1'].iloc[0],df['script2'].iloc[0],df['script3'].iloc[0],data['investment'],prices)
            except Exception:
                if str(traceback.format_exc()) not in errors:
                    logger.info(str(traceback.format_exc()))
                    errors.append(str(traceback.format_exc()))

        final_balance=binance_api.get_balance(client,data['tradable_base_coins'])

        if initial_balance!=0:
            profits=(final_balance-initial_balance) / initial_balance *100
        else:
            profits=0
        t={
            "time":datetime.now(),
            "base":df['base'].iloc[0],
            "script1":df['script1'].iloc[0],
            "script_price1":float(df['script_price1'].iloc[0]),
            "script2":df['script2'].iloc[0],
            "script_price2":float(df['script_price2'].iloc[0]),
            "script3":df['script3'].iloc[0],
            "script_price3":float(df['script_price3'].iloc[0]),
            "initial base account":float(df['initial base quantity'].iloc[0]),
            "final base quantity":float(df['final base quantity'].iloc[0]),
            "profits":float(profits)
        }

        trades.insert_one(t)

    print(df)
    df.to_csv("results.csv")


def run():
    delisted=find_delisted_coins()
    while True:

        # try:
            # print(f"checked {datetime.now()}")
            main()
        # except Exception:
        #     if str(str(traceback.format_exc())) not in errors:
        #         logger.info(str(traceback.format_exc()))
        #         errors.append(str(traceback.format_exc()))

if __name__=="__main__":
    delisted=find_delisted_coins()
    main()
    