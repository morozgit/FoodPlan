from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

def start_keyboard():
    button_data = [('Отлично!',),  ('Все пропало',)]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in button_data],
        resize_keyboard=True,
    )