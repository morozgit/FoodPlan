from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def start_keyboard():
    button_data = [("Отлично!",), ("Все пропало",)]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in button_data],
        resize_keyboard=True,
    )


def categories_keyboard(categories):
    builder = ReplyKeyboardBuilder()
    for category in categories:
        builder.add(KeyboardButton(text=category.name))

    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)


def dish_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Рецепт", callback_data="btn_recipe"))
    builder.row(
        InlineKeyboardButton(text="Предыдущее", callback_data="btn_prev_dish"),
        InlineKeyboardButton(text="Следующее", callback_data="btn_next_dish"),
    )
    return builder.as_markup()
