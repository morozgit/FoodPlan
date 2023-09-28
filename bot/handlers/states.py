from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    choose_category = State()
    choosing_category = State()  # выбор категории
