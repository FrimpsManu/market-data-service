from sqlalchemy.orm import Session
from datetime import datetime
from app.models.price import Price

def save_price(db: Session, symbol: str, price: float, timestamp: datetime):
    db_price = Price(symbol=symbol, value=price, timestamp=timestamp)
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

def get_latest_price(db: Session, symbol: str):
    return (
        db.query(Price)
        .filter(Price.symbol == symbol)
        .order_by(Price.timestamp.desc())
        .first()
    )
