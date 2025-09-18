from enum import StrEnum, auto


class MarketAction(StrEnum):
    update = auto()


class Scripts(StrEnum):
    discount_wb = auto()
    supplies_wb = auto()
