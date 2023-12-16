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
        data=admin.find_one()
        self.root=root
        self.root.title("Auto Trading Bot")
        self.admin=data['api_key']
        self.notebook=ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH,expand=True)

        self.tab1=ttk.Frame(self.notebook)
        self.tab2=ttk.Frame(self.notebook)

        self.notebook.add(self.tab1,text="Input Data")
        self.notebook.add(self.tab2,text="Present positions")

        self.tab1_fun()
        self.tab2_fun()

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
        
        self.admin=session.query(Admin).filter(Admin.id==1).first()

        self.label_API_KEY=tk.Label(self.tab1,text="API KEY")
        self.label_API_KEY.pack()

        self.entry_API_KEY=tk.Entry(self.tab1)
        self.entry_API_KEY.pack()
        self.entry_API_KEY.insert(0,self.admin.api_key)

        self.label_SECRET_KEY=tk.Label(self.tab1,text="SECRET KEY")
        self.label_SECRET_KEY.pack()

        self.entry_SECRET_KEY=tk.Entry(self.tab1)
        self.entry_SECRET_KEY.pack()
        self.entry_SECRET_KEY.insert(0,self.admin.secret_key)

        self.label_SYMBOL=tk.Label(self.tab1,text="SYMBOL")
        self.label_SYMBOL.pack()


        self.entry_SYMBOL=tk.Entry(self.tab1)
        self.entry_SYMBOL.pack()
        self.entry_SYMBOL.insert(0,self.admin.symbol)

        self.label_TAKEPROFIT=tk.Label(self.tab1,text="TAKE PROFIT")
        self.label_TAKEPROFIT.pack()


        self.entry_TAKEPROFIT=tk.Entry(self.tab1)
        self.entry_TAKEPROFIT.pack()
        self.entry_TAKEPROFIT.insert(0,self.admin.takeprofit)

        self.label_STOPLOSS=tk.Label(self.tab1,text="STOP LOSS")
        self.label_STOPLOSS.pack()


        self.entry_STOPLOSS=tk.Entry(self.tab1)
        self.entry_STOPLOSS.pack()
        self.entry_STOPLOSS.insert(0,self.admin.stoploss)

        self.submit=tk.Button(self.tab1,text="Submit",command=self.get_form_data)
        self.submit.pack()

        ttk.Separator(self.tab1, orient="horizontal").pack(pady=10)

        self.start=tk.Button(self.tab1,text="Start Strategy",command=self.start_strategy)
        self.start.pack()

        self.dot = tk.Label(self.tab1, text="●", font=("Helvetica", 36))
        self.dot.pack() 



    def start_strategy(self):
        self.dot.config(foreground="light green")

        admin=session.query(Admin).all()[0]
        admin.status=True
        session.commit()

        strat=Base_strategy(session)
        my_thread=threading.Thread(target=strat.run)
        my_thread.start()


    def get_form_data(self):

        api_key = self.entry_API_KEY.get()
        secret_key = self.entry_SECRET_KEY.get()
        symbol = self.entry_SYMBOL.get()
        take_profit = self.entry_TAKEPROFIT.get()
        stop_loss = self.entry_STOPLOSS.get()

        self.admin=session.query(Admin).filter(Admin.id==1).first()
        self.admin.api_key=api_key
        self.admin.secret_key=secret_key
        self.admin.symbol=symbol
        self.admin.takeprofit=int(take_profit)
        self.admin.stoploss=int(stop_loss)
        session.commit()


        # REFRESH 
        messagebox.showinfo("Information Updated", "The information has been updated")


def main():
    root=tk.Tk()
    app=App(root)
    root.mainloop()

if __name__=="__main__":
    main()