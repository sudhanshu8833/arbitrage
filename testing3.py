from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client1 = MongoClient(uri, server_api=ServerApi('1'),connect=False)
bot=client1['arbitrage']
admin=bot['admin']
trades=bot['trades']
screenshot=bot['screenshot']


bot1=client1['sudhanshu']
admin1=bot1['admin']
trades1=bot1['trades']
screenshot1=bot1['screenshot']
