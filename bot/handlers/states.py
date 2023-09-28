from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    CHOOSE_CATEGORY = State()
    CHOOSING_CATEGORY = State()  # выбор категории

    SHOW_RECIPE = State()
    SHOW_CATEGORIES = State()
    SHOW_INGREDIENTS = State()
    SHOW_DISHES = State()
    # ADD_FAVORITES = State()
    SHOW_FAVORITES = State()
    SHOW_PAY = State()
