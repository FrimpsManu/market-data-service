from pydantic import BaseModel
from typing import List, Optional

class PollRequest(BaseModel):
    symbols: List[str]
    interval: Optional[int] = 60  # in seconds
    provider: Optional[str] = "yfinance"
