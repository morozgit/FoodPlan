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
@router.message(States.show_categories)
async def get_categories(message: Message, state: FSMContext):
    await message.answer("Categories")
    await state.set_state(States.show_dishes)


@router.message(States.show_dishes)
async def get_dishes(message: Message, state: FSMContext):
    await message.answer("Dishes")
    await state.set_state(States.show_recipe)


@router.message(States.show_recipe)
async def get_recipe(message: Message, state: FSMContext):
    await message.answer("Recept")
    await state.set_state(States.show_ingredients)


@router.message(States.show_ingredients)
async def get_ingredients(message: Message, state: FSMContext):
    await message.answer("ingredients")
    await state.clear()


@router.message(States.show_favorites)
@router.message(Command(commands=["favorites"]))
async def get_favorites(message: Message, state: FSMContext):
    await message.answer("favorites")
    # await state.set_state(States.show_dishes) # todo


@router.message(States.show_pay)
async def get_pay(message: Message, state: FSMContext):
    await message.answer("pay")
