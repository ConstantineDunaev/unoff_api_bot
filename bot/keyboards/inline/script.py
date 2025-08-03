from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from bot.callback_factory import ScriptChoice
from enums import Scripts
from scripts import captions


def get_scripts_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for script in Scripts:
        builder.button(text=f'💥 {captions[script]}',
                       callback_data=ScriptChoice(script=script))
    return builder.adjust(1).as_markup()
