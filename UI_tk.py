import tkinter as tk
from tkinter import ttk,messagebox
from core.strategy import *
import threading

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'),connect=False)
bot=client['arbitrage']
admin=bot['admin']
trades=bot['trades']
screenshot=bot['screenshot']

class App:

    def __init__(self,root):
        self.root=root
        self.root.title("ARBITRAGE BOT")
        self.root.state("zoomed")
        self.admin=admin.find_one()
        self.notebook=ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH,expand=True)

        self.tab1=ttk.Frame(self.notebook)
        self.tab2=ttk.Frame(self.notebook)
        self.tab3=ttk.Frame(self.notebook)

        self.notebook.add(self.tab1,text="Input Data")
        self.notebook.add(self.tab2,text="Present positions")
        self.notebook.add(self.tab3,text="Market Snapshot")


        # T1=threading.Thread(target=self.tab1_fun)
        # T2=threading.Thread(target=self.tab2_fun)
        # T3=threading.Thread(target=self.tab3_fun)
        # T1.start()
        # T2.start()
        # T3.start()

        self.tab1_fun()
        self.tab2_fun()
        self.tab3_fun()

        self.root.after(0, self.update_page)

    def update_page(self):
        # print(self.present_position)

        T1=threading.Thread(target=self.populate_snapshot)
        T2=threading.Thread(target=self.populate_treeview)

        T1.start()
        T2.start()
        self.root.after(1000, self.update_page)


    def populate_treeview(self):
        # Query the database to fetch data from the Position table
        positions = list(trades.find({}))
        positions.reverse()

        # Update the existing list with the new positions
        existing_items = self.present_position.get_children()
        for i, position in enumerate(positions):
            values = (position['time'], position['base'], position['script1'], position['script_price1'], position['script2'], position['script_price2'], position['script3'], position['script_price3'],
                    position['initial base account'], position['final base quantity'], position['profits'])

            if i < len(existing_items):
                # Update existing item
                self.present_position.item(existing_items[i], values=values)
            else:
                # Insert new item at the end of the list
                self.present_position.insert("", "end", values=values)



    def tab2_fun(self):
        self.present_position=ttk.Treeview(self.tab2,columns=("Time","Base","script1","script_price1","script2","script_price2","script3","script_price3","initial quantity","final quantity","profits"),show="headings")
        self.present_position.heading("Time",text="Time")
        self.present_position.heading("Base",text="Base")
        self.present_position.heading("script1",text="script1")
        self.present_position.heading("script_price1",text="script_price1")
        self.present_position.heading("script2",text="script2")
        self.present_position.heading("script_price2",text="script_price2")
        self.present_position.heading("script3",text="script3")
        self.present_position.heading("script_price3",text="script_price3")
        self.present_position.heading("initial quantity",text="initial quantity")
        self.present_position.heading("final quantity",text="final quantity")
        self.present_position.heading("profits",text="profits")
        self.present_position.pack(fill="both",expand=True)
        T1=threading.Thread(target=self.populate_treeview)
        T1.start()



    def populate_snapshot(self):
        positions = list(screenshot.find({}))
        # positions.reverse()

        # Get the existing items in the Treeview
        existing_items = self.snapshot.get_children()

        # Iterate through the results and either update existing items or insert new ones
        for i, position in enumerate(positions):
            values = (position['time'], position['base'], position['script1'], position['script_price1'], position['script2'], position['script_price2'], position['script3'], position['script_price3'],
                    position['initial base quantity'], position['final base quantity'], position['profit'])

            if i < len(existing_items):
                # Update existing item
                self.snapshot.item(existing_items[i], values=values)
            else:
                # Insert new item at the end of the list
                self.snapshot.insert("", "end", values=values)

    def tab3_fun(self):
        self.snapshot=ttk.Treeview(self.tab3,columns=("Time","Base","script1","script_price1","script2","script_price2","script3","script_price3","initial quantity","final quantity","profits"),show="headings")
        self.snapshot.heading("Time",text="Time")
        self.snapshot.heading("Base",text="Base")
        self.snapshot.heading("script1",text="script1")
        self.snapshot.heading("script_price1",text="script_price1")
        self.snapshot.heading("script2",text="script2")
        self.snapshot.heading("script_price2",text="script_price2")
        self.snapshot.heading("script3",text="script3")
        self.snapshot.heading("script_price3",text="script_price3")
        self.snapshot.heading("initial quantity",text="initial quantity")
        self.snapshot.heading("final quantity",text="final quantity")
        self.snapshot.heading("profits",text="profits")
        self.snapshot.pack(fill="both",expand=True)
        T1=threading.Thread(target=self.populate_snapshot)
        T1.start()


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