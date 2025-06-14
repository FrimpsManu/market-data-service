from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.database import Base, engine

app = FastAPI(
    title="Market Data Service",
    description="Fetches market prices, computes moving averages, and serves APIs",
    version="0.1.0"
)

# Include API routes
app.include_router(api_router)

# Create tables on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
 
