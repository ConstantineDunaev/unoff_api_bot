from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from app.resource import Roles, Buttons
from app.enums import UserRole
from app.bot.callback_factory.role import ControlRole, RoleChoice
from app.bot.callback_factory.user import ControlUser, UserAction
from app.dto.chat import Chat
from app.dto.role import Role
from typing import List


def get_choice_role_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for role in UserRole:
        text = Roles[role]
        callback_data = RoleChoice(user_id=user_id,
                                   role=role.value)
        builder.button(text=text,
                       callback_data=callback_data)

    builder.button(text=Buttons.go_to_back,
                   callback_data=ControlUser(action=UserAction.view.value,
                                             user_id=user_id))
    return builder.adjust(1).as_markup()


def get_choice_role_chats_keyboard(user_id: int, role: int, chats: List[Chat],
                                   roles: List[Role]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for chat in chats:


    return builder.adjust(1).as_markup()
