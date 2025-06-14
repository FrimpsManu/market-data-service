from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import yfinance as yf
import uuid

from app.schemas.poll import PollRequest
from app.core.database import get_db
from app.services.crud import save_price
from app.models.price import Price

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/prices/poll", status_code=202)
def poll_prices(request: PollRequest, db: Session = Depends(get_db)):
    job_id = f"poll_{uuid.uuid4().hex[:8]}"
    prices = {}

    for symbol in request.symbols:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.history(period="1d")["Close"].iloc[-1]
            price = round(price, 2)
            prices[symbol] = price

            # Save each price to the DB
            save_price(db, symbol=symbol, price=price, timestamp=datetime.utcnow())
        except Exception as e:
            prices[symbol] = f"Error: {str(e)}"

    return {
        "job_id": job_id,
        "status": "accepted",
        "config": {
            "symbols": request.symbols,
            "interval": request.interval,
            "provider": request.provider
        },
        "prices": prices
    }

@router.get("/prices")
def get_prices(symbol: str, db: Session = Depends(get_db)):
    prices = (
        db.query(Price)
        .filter(Price.symbol == symbol)
        .order_by(Price.timestamp.desc())
        .limit(5)
        .all()
    )
    return [
        {
            "symbol": p.symbol,
            "value": p.value,
            "timestamp": p.timestamp.isoformat()
        }
        for p in prices
    ]
