from sqlalchemy.orm import Session
from app.models.price import Price
from datetime import datetime

def save_price(db: Session, symbol: str, price: float, timestamp: datetime):
    db_price = Price(symbol=symbol, price=price, timestamp=timestamp)
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
