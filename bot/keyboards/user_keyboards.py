from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def start_keyboard():
    button_data = [('Подписаться',)]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in button_data],
        resize_keyboard=True,
    )


def chose_subscription():
    buttons = [
        [InlineKeyboardButton(text="Неделя", callback_data="week")],
        [InlineKeyboardButton(text="Месяц", callback_data="month")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_main_menu():
    button_data = [('Главное меню',)]
