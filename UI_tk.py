import tkinter as tk
from tkinter import ttk,messagebox
from core.strategy import *
import threading

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
bot=client['arbitrage']
admin=bot['admin']
trades=bot['trades']

class App:

    def __init__(self,root):
        self.root=root
        self.root.title("ARBITRAGE BOT")
        self.admin=admin.find_one()
        self.notebook=ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH,expand=True)

        self.tab1=ttk.Frame(self.notebook)
        self.tab2=ttk.Frame(self.notebook)

        self.notebook.add(self.tab1,text="Input Data")
        self.notebook.add(self.tab2,text="Present positions")

        self.tab1_fun()
        # self.tab2_fun()

    def populate_treeview(self):
        # Clear existing data in the Treeview
        self.present_position.delete(*self.present_position.get_children())

        # Query the database to fetch data from the Position table
        positions = list(trades.find({}))
        positions.reverse()

        # Iterate through the results and insert them into the Treeview
        for position in positions:
            self.present_position.insert("", "end", values=(position.open_at, position.symbol, position.transaction,
                                          position.quantity, position.present_price, position.open_price, position.profit))

    def tab2_fun(self):
        self.present_position=ttk.Treeview(self.tab2,columns=("Time","symbol","Transaction","Quantity","present price","bought at","profit"),show="headings")
        self.present_position.heading("Time",text="Time")
        self.present_position.heading("symbol",text="symbol")
        self.present_position.heading("Transaction",text="Transaction")
        self.present_position.heading("Quantity",text="Quantity")
        self.present_position.heading("present price",text="present price")
        self.present_position.heading("bought at",text="bought at")
        self.present_position.heading("profit",text="profit")
        self.present_position.pack()
        self.populate_treeview()

    def tab1_fun(self):
        
        self.admin=admin.find_one()

        # self.label_API_KEY=tk.Label(self.tab1,text="API KEY")
        # self.label_API_KEY.pack()

        # self.entry_API_KEY=tk.Entry(self.tab1)
        # self.entry_API_KEY.pack()
        # self.entry_API_KEY.insert(0,self.admin.api_key)

        # self.label_SECRET_KEY=tk.Label(self.tab1,text="SECRET KEY")
        # self.label_SECRET_KEY.pack()

        # self.entry_SECRET_KEY=tk.Entry(self.tab1)
        # self.entry_SECRET_KEY.pack()
        # self.entry_SECRET_KEY.insert(0,self.admin.secret_key)

        self.label_EXCHANGE=tk.Label(self.tab1,text="EXCHANGE")
        self.label_EXCHANGE.pack()

        self.entry_EXCHANGE=tk.Entry(self.tab1)
        self.entry_EXCHANGE.pack()
        self.entry_EXCHANGE.insert(0,self.admin['exchange'])

        ttk.Separator(self.tab1, orient="horizontal").pack(pady=10)

        self.label_BASE=tk.Label(self.tab1,text="BASE")
        self.label_BASE.pack()

        self.entry_BASE=tk.Entry(self.tab1)
        self.entry_BASE.pack()
        self.entry_BASE.insert(0,self.admin['tradable_base_coins'])

        ttk.Separator(self.tab1, orient="horizontal").pack(pady=10)

        self.label_INVESTMENT=tk.Label(self.tab1,text="INVESTMENT % OF PORTFOLIO")
        self.label_INVESTMENT.pack()

        self.entry_INVESTMENT=tk.Entry(self.tab1)
        self.entry_INVESTMENT.pack()
        self.entry_INVESTMENT.insert(0,self.admin['investment'])

        ttk.Separator(self.tab1, orient="horizontal").pack(pady=10)

        self.label_min_profit=tk.Label(self.tab1,text="MINIMUM PROFIT")
        self.label_min_profit.pack()


        self.entry_min_profit=tk.Entry(self.tab1)
        self.entry_min_profit.pack()
        self.entry_min_profit.insert(0,self.admin['minimum_profit'])

        ttk.Separator(self.tab1, orient="horizontal").pack(pady=10)


        # self.check_button1 = tk.Checkbutton(self.tab1)
        # self.check_button1.pack()
        # self.check_button1.insert(0,self.admin['paper_trading'])
        self.paper_trading_var = tk.BooleanVar(value=self.admin['paper_trading'])
        self.check_button1 = tk.Checkbutton(self.tab1, text="Paper Trading", variable=self.paper_trading_var)
        self.check_button1.pack()

        ttk.Separator(self.tab1, orient="horizontal").pack(pady=10)

        self.submit=tk.Button(self.tab1,text="Submit",command=self.get_form_data)
        self.submit.pack()

        ttk.Separator(self.tab1, orient="horizontal").pack(pady=10)

        self.start=tk.Button(self.tab1,text="Start Strategy",command=self.start_strategy)
        self.start.pack()
        self.dot = tk.Label(self.tab1, text="●", font=("Helvetica", 36))
        self.dot.pack() 
        # self.dot = tk.Label(self.tab1, text="●", font=("Helvetica", 36))
        # self.dot.pack() 



    def start_strategy(self):
        self.dot.config(foreground="light green")
        my_thread=threading.Thread(target=run)
        my_thread.start()


    def get_form_data(self):

        exchange = self.entry_EXCHANGE.get()
        base = self.entry_BASE.get()
        investment = self.entry_INVESTMENT.get()
        min_profit = self.entry_min_profit.get()
        paper = self.paper_trading_var.get()

        self.admin=admin.find_one()
        self.admin['exchange']=exchange
        self.admin['tradable_base_coins']=base
        self.admin['investment']=float(investment)
        self.admin['minimum_profit']=float(min_profit)
        self.admin['paper_trading']=paper
        print(self.admin)

        admin.update_one({},{'$set':self.admin})

        messagebox.showinfo("Information Updated", "The information has been updated")


def main():
    root=tk.Tk()
    app=App(root)
    root.mainloop()

if __name__=="__main__":
    main()