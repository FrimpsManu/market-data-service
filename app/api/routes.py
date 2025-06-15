from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from celery.result import AsyncResult

from app.schemas.poll import PollRequest
from app.schemas.price import PriceResponse
from app.core.database import get_db
from app.models.price import Price
from app.models.symbol_average import SymbolAverage  # ✅ add this
from app.services import crud
from worker import celery_app

router = APIRouter()

# ✅ Health check
@router.get("/health")
def health():
    return {"status": "ok"}

# ✅ Poll prices using Celery task
@router.post("/prices/poll", status_code=202)
def poll_prices(request: PollRequest):
    task = celery_app.send_task(
        "poll_and_store_prices",
        args=[request.symbols],
        kwargs={"provider": request.provider}
    )
    job_id = task.id
    return {
        "job_id": job_id,
        "celery_id": task.id,
        "status": "started",
        "config": {
            "symbols": request.symbols,
            "interval": request.interval,
            "provider": request.provider
        }
    }

# ✅ Get latest price for a symbol
@router.get("/prices/latest", response_model=PriceResponse)
def get_latest_price(symbol: str, db: Session = Depends(get_db)):
    price = crud.get_latest_price(db, symbol=symbol)
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return {
        "symbol": price.symbol,
        "value": price.value,
        "timestamp": price.timestamp,
        "provider": "yfinance"
    }

# ✅ Get last 5 price points for a symbol
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

# ✅ Celery task status lookup
@router.get("/prices/status/{job_id}")
def get_poll_status(job_id: str):
    result = AsyncResult(job_id, app=celery_app)
    return {
        "job_id": job_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

# ✅ Get latest moving average for a symbol
@router.get("/averages/latest")
def get_latest_moving_average(symbol: str, db: Session = Depends(get_db)):
    avg = (
        db.query(SymbolAverage)
        .filter(SymbolAverage.symbol == symbol)
        .order_by(SymbolAverage.timestamp.desc())
        .first()
    )
    if not avg:
        raise HTTPException(status_code=404, detail="No moving average found for symbol")
    return {
        "symbol": avg.symbol,
        "moving_average": avg.moving_average,
        "timestamp": avg.timestamp.isoformat()
    }
