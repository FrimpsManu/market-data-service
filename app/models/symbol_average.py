from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base

class SymbolAverage(Base):
    __tablename__ = "symbol_averages"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    moving_average = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
