from sqlalchemy import Column, String, Float, DateTime
from app.core.database import Base
from datetime import datetime
import uuid

class PricePoint(Base):
    __tablename__ = "price_points"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    provider = Column(String, nullable=False)
