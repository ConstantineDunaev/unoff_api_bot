from aiogram.filters.callback_data import CallbackData
from enums import MarketAction


class MarketControl(CallbackData, prefix="market"):
    action: MarketAction
    market_id: int
