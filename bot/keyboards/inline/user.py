from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from app.dto.user import User
from app.resource import Buttons
from app.bot.callback_factory.user import ControlUser, UserAction


def get_control_employee_keyboard(employee: User) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if employee.username:
        builder.button(text=Buttons.go_to_employee, url=f"https://t.me/{employee.username}")

    callback_data = ControlUser(action=UserAction.disable_query, user_id=employee.user_id)
    builder.button(text=Buttons.disable_employee, callback_data=callback_data)

    callback_data = ControlUser(action=UserAction.roles, user_id=employee.user_id)
    builder.button(text=Buttons.control_roles, callback_data=callback_data)

    return builder.adjust(1).as_markup()


def get_query_employee_disable_keyboard(employee: User) -> InlineKeyboardMarkup:
    callback_data_yes = ControlUser(action=UserAction.disable_confirm.value,
                                    user_id=employee.user_id)
    button_yes = InlineKeyboardButton(text=Buttons.confirm_yes,
                                      callback_data=callback_data_yes.pack())

    callback_data_no = ControlUser(action=UserAction.view.value,
                                   user_id=employee.user_id)
    button_no = InlineKeyboardButton(text=Buttons.confirm_no,
                                     callback_data=callback_data_no.pack())

    builder = InlineKeyboardBuilder()
    builder.add(button_yes, button_no)
    return builder.adjust(2).as_markup()
