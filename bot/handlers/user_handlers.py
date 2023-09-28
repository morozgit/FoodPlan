from aiogram import Bot, Router
from aiogram.filters import CommandStart, Text
from bot.config_data.config import load_config
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.keyboards import user_keyboards
from bot.handlers.states import UserStates


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
    await state.set_state(UserStates.choosing_category)
