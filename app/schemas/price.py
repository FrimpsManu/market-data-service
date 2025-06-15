from pydantic import BaseModel
from datetime import datetime

class PriceResponse(BaseModel):
    symbol: str
    value: float
    timestamp: datetime
    provider: str

    class Config:
        orm_mode = True
