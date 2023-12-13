from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float,Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
# Specify the path to your SQLite database file
db_path = "./app.db"

# Create an SQLite database engine
engine = create_engine(f"sqlite:///{db_path}")

Base = declarative_base()

class Admin(Base):
    __tablename__ = "Admin"
    id=Column(Integer,primary_key=True,autoincrement=True)
    api_key = Column(String)
    secret_key = Column(String)
    symbol=Column(String)
    takeprofit = Column(Integer)
    stoploss=Column(Integer)
    status=Column(Boolean,default=False)


class Position(Base):
    __tablename__ = "Position"
    id=Column(Integer,primary_key=True,autoincrement=True)
    open_at = Column(DateTime, default=datetime.utcnow())
    symbol = Column(String)
    transaction=Column(String,default="LONG") # LONG / SHORT
    quantity = Column(Integer,default=1)
    present_price=Column(Float)
    open_price=Column(Float)
    close_price=Column(Float,default=-1)
    open_at = Column(DateTime, default=None)
    profit=Column(Float,default=0)
    Status=Column(String,default="OPEN") # OPEN / CLOSE


# Tkinter
# SQLalchemy
# 

