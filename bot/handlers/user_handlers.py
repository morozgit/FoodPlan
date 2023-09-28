from aiogram import Bot, Router
from bot.config_data.config import load_config
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.keyboards import user_keyboards
from bot.handlers.states import States


router = Router()
config = load_config()
admin_ids = config.admins.ids


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text="Привет как дела",
        reply_markup=user_keyboards.start_keyboard(),
    )

    user_id = int(message.from_user.id)
    await state.update_data(prods=[])
    await state.update_data(user_id=user_id)
    await state.set_state(States.choosing_category)


@router.message(Command(commands=["categories", "start"]))
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


@router.message(States.SHOW_FAVORITES)
@router.message(Command(commands=["favorites"]))
async def get_favorites(message: Message, state: FSMContext):
    await message.answer("favorites")
    # await state.set_state(States.SHOW_DISHES) # todo


@router.message(States.SHOW_PAY)
async def get_pay(message: Message, state: FSMContext):
    await message.answer("pay")
