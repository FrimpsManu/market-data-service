from celery import Celery
import yfinance as yf
from datetime import datetime
from app.core.database import SessionLocal
from app.services.crud import save_price

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

@celery_app.task(name="poll_and_store_prices")
def poll_and_store_prices(symbols: list[str], provider: str = "yfinance"):
    db = SessionLocal()
    results = {}

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.history(period="1d")["Close"].iloc[-1]
            price = round(price, 2)
            save_price(db, symbol=symbol, price=price, timestamp=datetime.utcnow())
            results[symbol] = price
        except Exception as e:
            results[symbol] = f"Error: {str(e)}"

    db.close()
    return results
