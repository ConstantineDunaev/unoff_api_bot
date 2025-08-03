from dataclasses import dataclass, asdict, astuple
from datetime import datetime


@dataclass
class NewMarket:
    name: str
    headers: str
    cookies: str
    is_active: bool
    updated_at: datetime

    def as_tuple(self) -> tuple:
        return astuple(self)


@dataclass
class Market:
    market_id: int
    name: str
    headers: dict
    cookies: dict
    is_active: bool
    updated_at: datetime

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class UpdateMarket:
    name: str
    headers: dict
    cookies: dict
    is_active: bool
    updated_at: datetime
    market_id: int

    def as_tuple(self) -> tuple:
        return astuple(self)


@dataclass
class GetMarket:
    market_id: int

    def as_tuple(self) -> tuple:
        return astuple(self)
