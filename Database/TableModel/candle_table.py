from sqlalchemy import Column, Integer, String, Numeric, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class candles_table(Base):
    
    __tablename__ = "Candles"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Symbol = Column(String(10), nullable=False)
    Interval = Column(String(10), nullable=False)
    OpenTime = Column(BigInteger, nullable=False)
    Open = Column(Numeric(18,8), nullable=False)
    High = Column(Numeric(18,8), nullable=False)
    Low = Column(Numeric(18,8), nullable=False)
    Close = Column(Numeric(18,8), nullable=False)
    Volume = Column(Numeric(18,8), nullable=False)
    CloseTime = Column(BigInteger, nullable=False)
    