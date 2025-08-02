from dataclasses import dataclass
from datetime import datetime


@dataclass
class Market:
    market_id: int
    name: str
    headers: dict
    cookies: dict
    is_active: bool
    updatet_at: datetime
