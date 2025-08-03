from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from schemas.market import Market
from bot.resources import Buttons
from bot.callback_factory import MarketControl
from enums import MarketAction


def get_market_control_keyboard(market: Market) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=Buttons.update_market, callback_data=MarketControl(action=MarketAction.update,
                                                                           market_id=market.market_id))
    return builder.adjust(1).as_markup()
