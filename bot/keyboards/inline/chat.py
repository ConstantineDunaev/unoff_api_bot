from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from app.dto.chat import Chat
from app.resource import Buttons
from app.bot.callback_factory.chat import ControlChat, ChatAction


def get_control_chat_keyboard(chat: Chat) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    text = Buttons.go_to_chat.format(title=chat.title)
    chat_id = str(chat.chat_id).replace("-100", "")
    url = f'https://t.me/c/{chat_id}'
    builder.button(text=text,
                   url=url)

    if chat.is_active:
        callback_data = ControlChat(action=ChatAction.deactivate,
                                    chat_id=chat.chat_id)
        builder.button(text=Buttons.deactivate_chat,
                       callback_data=callback_data)
    else:
        callback_data = ControlChat(action=ChatAction.activate,
                                    chat_id=chat.chat_id)
        builder.button(text=Buttons.activate_chat,
                       callback_data=callback_data)

        callback_data = ControlChat(action=ChatAction.delete_query,
                                    chat_id=chat.chat_id)
        builder.button(text=Buttons.delete_chat,
                       callback_data=callback_data)

    return builder.adjust(1).as_markup()


def get_delete_chat_query_keyboard(chat: Chat) -> InlineKeyboardMarkup:
    callback_data_yes = ControlChat(action=ChatAction.delete_confirm.value,
                                    chat_id=chat.chat_id)
    button_yes = InlineKeyboardButton(text=Buttons.confirm_yes,
                                      callback_data=callback_data_yes.pack())

    callback_data_no = ControlChat(action=ChatAction.view.value,
                                   chat_id=chat.chat_id)
    button_no = InlineKeyboardButton(text=Buttons.confirm_no,
                                     callback_data=callback_data_no.pack())

    builder = InlineKeyboardBuilder()
    builder.add(button_yes, button_no)
    return builder.adjust(2).as_markup()
