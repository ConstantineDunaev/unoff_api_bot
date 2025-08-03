from aiogram.filters.callback_data import CallbackData
from enum import StrEnum
from typing import Optional


class RoleChoice(CallbackData, prefix="choice"):
    user_id: int
    role: int


class RoleUpdateEnum(StrEnum):
    set = "set"
    unset = "unset"


class ControlRole(CallbackData, prefix="control"):
    action: RoleUpdateEnum
    chat_id: int
    user_id: int
    role: int
