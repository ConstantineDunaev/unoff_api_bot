from aiogram.filters.callback_data import CallbackData
from enum import StrEnum


class UserAction(StrEnum):
    disable_query = "disable_query"
    disable_confirm = "disable_confirm"
    roles = "roles"
    view = "view"


class ControlUser(CallbackData, prefix="user"):
    action: UserAction
    user_id: int
