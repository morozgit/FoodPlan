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
    show_subscription = State()
    show_subscription_1_week = State()
    show_subscription_1_month = State()
    show_pay = State()
    show_successful_payment = State()
