from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    choose_category = State()
    choosing_category = State()  # выбор категории

    show_recipe = State()
    show_categories = State()
    show_ingredients = State()
    show_dishes = State()
    # add_favorites = State()
    show_favorites = State()
    show_pay = State()

    show_favorite = State()