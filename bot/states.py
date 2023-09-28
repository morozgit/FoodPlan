from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    SHOW_RECIPE = State()
    SHOW_CATEGORIES = State()
    SHOW_INGREDIENTS = State()
    SHOW_DISHES = State()

    # ADD_FAVORITES = State()
    SHOW_FAVORITES = State()
