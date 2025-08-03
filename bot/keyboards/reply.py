from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.resources import Buttons


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=Buttons.markets)
    builder.button(text=Buttons.scripts)
    return builder.adjust(1).as_markup(resize_keyboard=True)


def get_markets_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=Buttons.add_market)
    builder.button(text=Buttons.list_markets)
    builder.button(text=Buttons.back)
    return builder.adjust(1).as_markup(resize_keyboard=True)


def get_back_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=Buttons.back)
    return builder.adjust(1).as_markup(resize_keyboard=True)
