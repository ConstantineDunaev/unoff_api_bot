from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NewJob:
    market_id: int
    start: datetime
    script_name: str
    params: Optional[str] = None


@dataclass
class Job:
    job_id: int
    market_id: int
    start: datetime
    script_name: str
    params: Optional[str] = None
    finish: Optional[datetime] = None


@dataclass
class FinishJob:
    job_id: int
    fihish: datetime


