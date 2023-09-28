from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .states import States

router = Router()


@router.message(CommandStart())
@router.message(States.SHOW_CATEGORIES)
async def get_categories(message: Message, state: FSMContext):
    await message.answer("Categories")
    await state.set_state(States.SHOW_DISHES)


@router.message(States.SHOW_DISHES)
async def get_dishes(message: Message, state: FSMContext):
    await message.answer("Dishes")
    await state.set_state(States.SHOW_RECIPE)


@router.message(States.SHOW_RECIPE)
async def get_recipe(message: Message, state: FSMContext):
    await message.answer("Recept")
    await state.set_state(States.SHOW_INGREDIENTS)


@router.message(States.SHOW_INGREDIENTS)
async def get_ingredients(message: Message, state: FSMContext):
    await message.answer("ingredients")
    await state.clear()


@router.message(Command(commands=["favorites"]))
async def get_favorites(message: Message, state: FSMContext):
    await message.answer("favorites")
    # await state.set_state(States.SHOW_DISHES) # todo
