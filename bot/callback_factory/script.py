from aiogram.filters.callback_data import CallbackData
from enums import Scripts


class ScriptChoice(CallbackData, prefix="script"):
    script: Scripts

