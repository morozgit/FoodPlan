from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto, BufferedInputFile
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async
from bot.config_data.config import load_config
from bot.handlers.states import States
from bot.keyboards import user_keyboards
from bot.models import Category, Dish

router = Router()
config = load_config()
admin_ids = config.admins.ids


@router.message(Command(commands=["categories", "start"]))
@router.message(States.show_categories)
async def get_categories(message: Message, state: FSMContext):
    categories = await sync_to_async(Category.objects.all)()
    await message.reply(
        "Выберите категорию:",
        reply_markup=user_keyboards.categories_keyboard(categories),
    )
    await state.set_state(States.show_dishes)


@router.message(States.show_dishes)
async def get_dishes(message: Message, state: FSMContext):
    selected_category = message.text
    await state.update_data(selected_category=selected_category)

    dish = await sync_to_async(Dish.objects.first)()
    photo = FSInputFile(dish.image.path)
    posted_dish = await message.answer_photo(
        photo,
        caption=dish.name,
        reply_markup=user_keyboards.dish_keyboard()
    )
    await state.update_data(
        dish_id=dish.id,
        posted_dish=posted_dish
    )
    # await state.set_state(States.show_recipe)


@router.callback_query(F.data == "btn_next_dish")
@router.callback_query(F.data == "btn_prev_dish")
@router.callback_query(F.data == "btn_current_dish")
async def next_dish(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    posted_dish = state_data.get("posted_dish")
    dish_id = state_data.get("dish_id")

    dish = None
    if callback.data == "btn_next_dish":
        dish = Dish.objects.filter(id__gt=dish_id).order_by('id').first()
    elif callback.data == "btn_prev_dish":
        dish = Dish.objects.filter(id__lt=dish_id).order_by('id').first()
    elif callback.data == "btn_current_dish":
        dish = Dish.objects.get(pk=dish_id)

    if not dish:
        await callback.answer()
        await callback.message.answer(text="Товаров больше нет. Выберите из другой категории.", reply_markup=None)
        return

    await state.update_data(dish_id=dish.id)

    new_media = InputMediaPhoto(
        media=BufferedInputFile.from_file(dish.image.path),
        caption=dish.name
    )
    await posted_dish.edit_media(
        media=new_media,
        inline_message_id=str(posted_dish.message_id),
        reply_markup=user_keyboards.dish_keyboard()
    )


@router.callback_query(F.data == "btn_recipe")
async def clicked_recipe(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    dish_id = state_data.get("dish_id")
    dish = await sync_to_async(Dish.objects.get)(id=dish_id)
    photo = FSInputFile(dish.image.path)
    caption = f'''{dish.name}

    {dish.description}

'''
    posted_dish = await callback.message.answer_photo(
        photo,
        caption=caption,
        reply_markup=user_keyboards.dish_detail_keyboard()
    )
    ingridients = dish.ingridients
    print(ingridients)
    await state.update_data(
        dish_id=dish.id,
        posted_dish=posted_dish
    )


# @router.message(States.show_recipe)
# async def get_recipe(message: Message, state: FSMContext):
#     # await message.answer("Recept")
#     # await state.set_state(States.show_ingredients)


@router.message(States.show_ingredients)
async def get_ingredients(message: Message, state: FSMContext):
    await message.answer("ingredients")
    await state.clear()


@router.message(States.show_favorites)
@router.message(Command(commands=["favorites"]))
async def get_favorites(message: Message, state: FSMContext):
    await message.answer("favorites")
    await state.set_state(States.show_dishes)  # todo


@router.message(States.show_pay)
async def get_pay(message: Message, state: FSMContext):
    await message.answer("pay")

    await state.set_state(UserStates.choosing_category)
