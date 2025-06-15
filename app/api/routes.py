from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.poll import PollRequest
from app.core.database import get_db
from app.models.price import Price
from worker import celery_app
from celery.result import AsyncResult

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

# ✅ Celery-based price polling
@router.post("/prices/poll", status_code=202)
def poll_prices(request: PollRequest):
    task = celery_app.send_task(
        "poll_and_store_prices",
        args=[request.symbols],
        kwargs={"provider": request.provider}
    )
    job_id = task.id  # Use Celery's actual task ID for tracking

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

# ✅ Task status lookup
@router.get("/prices/status/{job_id}")
def get_poll_status(job_id: str):
    result = AsyncResult(job_id, app=celery_app)
    return {
        "job_id": job_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }
