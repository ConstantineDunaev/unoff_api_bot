from aiogram.filters.callback_data import CallbackData
from enum import StrEnum


class ChatAction(StrEnum):
    activate = "activate"
    deactivate = "deactivate"
    delete_query = "delete_query"
    delete_confirm = "delete_confirm"
    view = "view"


class ControlChat(CallbackData, prefix="chat"):
    action: ChatAction
    chat_id: int
