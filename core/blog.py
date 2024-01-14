import core.binance_api as binance_api
import traceback
import math
import logging
from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import os
import sys

database='arbitrage'

logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client1 = MongoClient(uri, server_api=ServerApi('1'),connect=False)
bot=client1[database]
admin=bot['admin']

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

errors=[]

def check_if_float_zero(value):
    return math.isclose(value, 0.0, abs_tol=1e-3)

def check_profit_loss(total_price_after_sell,initial_investment,transaction_brokerage,minimum_profit):
    # print(total_price_after_sell,initial_investment,transaction_brokerage)
    apprx_brokerage = transaction_brokerage * (initial_investment/100) * 3
    min_profitable_price = initial_investment + apprx_brokerage
    profit_loss = float(total_price_after_sell) - float(min_profitable_price)

    profit_loss_per=(profit_loss/initial_investment)*100
    # print(profit_loss,profit_loss_per)
    final_value=total_price_after_sell-apprx_brokerage
    return profit_loss_per,final_value

def get_crypto_combinations(market_symbols, base):
    combinations = []
    for sym1 in market_symbols:   
        sym1_token1 = sym1.split('/')[0]
        sym1_token2 = sym1.split('/')[1]
        if (sym1_token2 == base):
            for sym2 in market_symbols:
                sym2_token1 = sym2.split('/')[0]
                sym2_token2 = sym2.split('/')[1]
                if (sym1_token1 == sym2_token2):
                    for sym3 in market_symbols:
                        sym3_token1 = sym3.split('/')[0]
                        sym3_token2 = sym3.split('/')[1]
                        if((sym2_token1 == sym3_token1) and (sym3_token2 == sym1_token2)):
                            combination = {
                                'base':sym1_token2,
                                'intermediate':sym1_token1,
                                'ticker':sym2_token1,
                            }
                            combinations.append(combination)

    return combinations

def check_buy_buy_sell(scrip1, scrip2, scrip3,initial_investment,prices):
    
    ## SCRIP1
    investment_amount1 = initial_investment
    current_price1 = float(prices[scrip1]['ask'])
    final_price = 0
    scrip_prices = {}
    
    if current_price1 is not None and not check_if_float_zero(current_price1):
        buy_quantity1 = round(investment_amount1 / current_price1, 8)

        ## SCRIP2
        investment_amount2 = buy_quantity1     
        current_price2 = float(prices[scrip2]['ask'])
        if current_price2 is not None and not check_if_float_zero(current_price2):
            buy_quantity2 = round(investment_amount2 / current_price2, 8)
            
            ## SCRIP3
            investment_amount3 = buy_quantity2     
            current_price3 = float(prices[scrip3]['bid'])
            if current_price3 is not None and not check_if_float_zero(current_price3):
                sell_quantity3 = buy_quantity2
                final_price = round(sell_quantity3 * current_price3,3)
                scrip_prices = {scrip1 : current_price1, scrip2 : current_price2, scrip3 : current_price3}
                
    return final_price, scrip_prices

def check_buy_sell_sell(scrip1, scrip2, scrip3,initial_investment,prices):

    ## SCRIP1
    investment_amount1 = initial_investment
    current_price1 = float(prices[scrip1]['ask'])
    final_price = 0
    scrip_prices = {}
    if current_price1 is not None and not check_if_float_zero(current_price1):
        buy_quantity1 = round(investment_amount1 / current_price1, 8)

        ## SCRIP2
        investment_amount2 = buy_quantity1     
        current_price2 = float(prices[scrip2]['bid'])
        if current_price2 is not None and not check_if_float_zero(current_price2):
            sell_quantity2 = buy_quantity1
            sell_price2 = round(sell_quantity2 * current_price2,8)

            ## SCRIP1
            investment_amount3 = sell_price2     
            current_price3 = float(prices[scrip3]['bid'])
            if current_price3 is not None and not check_if_float_zero(current_price3):
                sell_quantity3 = sell_price2
                final_price = round(sell_quantity3 * current_price3,3)
                scrip_prices = {scrip1 : current_price1, scrip2 : current_price2, scrip3 : current_price3}
    return final_price,scrip_prices

def place_buy_order(client,scrip, quantity):
    order = binance_api.market_order(client,scrip,"BUY","MARKET", quantity)
    return order['fills'][0]['price']

def place_sell_order(client,scrip, quantity):
    order = binance_api.market_order(client,scrip,"SELL","MARKET", quantity)
    return order['fills'][0]['price']

def place_trade_orders(client,type, script, initial_amount, scrip_prices,base_symbols,data):



    if type == 'BUY_BUY_SELL':

        # 1. BTC USDT 2. ETH BTC 3. ETH USDT

        s1_quantity=initial_amount
        price1=place_buy_order(client,script[0], s1_quantity)


        s2_quantity=binance_api.get_balance(client,base_symbols[1])
        price2=place_buy_order(client,script[1], s2_quantity)


        s3_quantity=binance_api.get_balance(client,base_symbols[2])
        price3=place_sell_order(client,script[2], s3_quantity)

        return price1,price2,price3


    elif type == 'BUY_SELL_SELL':

        # 1. BTCUSDT 2. BTCETH 3. ETHUSDT
        # USDT BTC ETH 

        s1_quantity=initial_amount
        price1=place_buy_order(client,script[0], s1_quantity)

        s2_quantity=binance_api.get_balance(client,base_symbols[2])
        price2=place_sell_order(client,script[1], s2_quantity)

        s3_quantity=binance_api.get_balance(client,base_symbols[1])
        price3=place_sell_order(client,script[2], s3_quantity)

        return price1,price2,price3
        
    