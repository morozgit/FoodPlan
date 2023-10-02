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


def dish_keyboard(should_add_favorite=True):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Рецепт", callback_data="recipe_btn"))

    if should_add_favorite:
        builder.row(InlineKeyboardButton(text="Добавить в избранное", callback_data="add_favorite_btn"))
    else:
        builder.row(InlineKeyboardButton(text="Удалить из избранного", callback_data="remove_favorite_btn"))

    builder.row(
        InlineKeyboardButton(text="Предыдущее", callback_data="prev_dish_btn"),
        InlineKeyboardButton(text="Следующее", callback_data="next_dish_btn"),
    )
    return builder.as_markup()


def dish_detail_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад",
                                     callback_data="btn_current_dish"))


