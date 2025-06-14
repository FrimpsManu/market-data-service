from celery import Celery
from app.core.database import SessionLocal
from app.services.crud import save_price
import yfinance as yf
from datetime import datetime

app = Celery("worker", broker="kafka://kafka:9092")

@app.task
def fetch_and_store_price(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.history(period="1d")["Close"].iloc[-1]
        db = SessionLocal()
        save_price(db, symbol=symbol, price=round(price, 2), timestamp=datetime.utcnow())
        db.close()
        return {"symbol": symbol, "price": price}
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}
