from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto, BufferedInputFile
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async
from bot.config_data.config import load_config
from bot.handlers.states import States
from bot.keyboards import user_keyboards
from bot.models import Dish, BotUser, ReceptItem
from django.db.models import Q


router = Router()
config = load_config()
admin_ids = config.admins.ids


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    user, created = BotUser.objects.get_or_create(
        name=message.from_user.username, tig_id=message.from_user.id
    )
    if not created:
        await message.answer(
            text=f"C возращением! {user.name}. Выберите категорию:",
            reply_markup=user_keyboards.categories_keyboard(),
        )
    else:
        await message.answer(
            text=f"Добро пожаловать! {user.name}. Выберите категорию:",
            reply_markup=user_keyboards.categories_keyboard(),
        )
    await state.set_state(States.show_dishes)


@router.message(Command(commands=["categories"]))
@router.message(States.show_categories)
async def get_categories(message: Message, state: FSMContext):
    await message.reply(
        "Выберите категорию:",
        reply_markup=user_keyboards.categories_keyboard(),
    )
    await state.set_state(States.show_dishes)


@router.message(States.show_dishes)
async def get_dishes(message: Message, state: FSMContext):
    selected_category = message.text
    await state.update_data(selected_category=selected_category)

    dish = await sync_to_async(Dish.objects.first)()
    photo = FSInputFile(dish.image.path)
    posted_dish = await message.answer_photo(
        photo, caption=dish.name, reply_markup=user_keyboards.dish_keyboard()
    )
    await state.update_data(dish_id=dish.id, posted_dish=posted_dish)
    # await state.set_state(States.show_recipe)


@router.callback_query(F.data == "next_dish_btn")
@router.callback_query(F.data == "prev_dish_btn")
@router.callback_query(F.data == "btn_current_dish")
async def next_dish(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    posted_dish = state_data.get("posted_dish")
    dish_id = state_data.get("dish_id")

    dish = None
    if callback.data == "next_dish_btn":
        dish = Dish.objects.filter(id__gt=dish_id).order_by("id").first()
    elif callback.data == "prev_dish_btn":
        dish = Dish.objects.filter(id__lt=dish_id).order_by("id").first()
    elif callback.data == "btn_current_dish":
        dish = Dish.objects.get(pk=dish_id)

    if not dish:
        await callback.answer()
        await callback.message.answer(
            text="Товаров больше нет. Выберите из другой категории.", reply_markup=None
        )
        return

    await state.update_data(dish_id=dish.id)

    new_media = InputMediaPhoto(
        media=BufferedInputFile.from_file(dish.image.path), caption=dish.name
    )
    await posted_dish.edit_media(
        media=new_media,
        inline_message_id=str(posted_dish.message_id),
        reply_markup=user_keyboards.dish_keyboard(),
    )


@router.callback_query(F.data == "recipe_btn")
async def clicked_recipe(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    dish_id = state_data.get("dish_id")
    dish = await sync_to_async(Dish.objects.get)(id=dish_id)
    photo = FSInputFile(dish.image.path)
    caption = f"""{dish.name}

    {dish.description}

"""

    recept = ReceptItem.objects.filter(dish=dish_id).all()
    recept_text = "ИНГРИДИЕНТЫ \n\n"
    for ing in recept:
        recept_text += f"{ing.ingridient.name} - {ing.quantity} {ing.unit} ({ing.ingridient.price} ₽)\n"

    posted_dish = await callback.message.answer_photo(
        photo, caption=recept_text, reply_markup=user_keyboards.dish_detail_keyboard()
    )
    await callback.message.answer(text=caption, reply_markup=None)
    await state.update_data(dish_id=dish.id, posted_dish=posted_dish)


@router.callback_query(F.data == "add_favorite_btn")
async def add_favorite(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    posted_dish = state_data.get("posted_dish")
    dish_id = state_data.get("dish_id")

    user = BotUser.objects.get(tig_id=callback.from_user.id)
    user.favorites.set([dish_id, *user.favorites.all()])
    await callback.answer("Добавлено в избранное")

    await posted_dish.edit_reply_markup(
        inline_message_id=str(posted_dish.message_id),
        reply_markup=user_keyboards.dish_keyboard(should_add_favorite=False),
    )


@router.callback_query(F.data == "remove_favorite_btn")
async def remove_favorite(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    posted_dish = state_data.get("posted_dish")
    dish_id = state_data.get("dish_id")

    user = BotUser.objects.get(tig_id=callback.from_user.id)
    user.favorites.set([*user.favorites.filter(~Q(id=dish_id))])
    await callback.answer("Удалено из избранного")

    await posted_dish.edit_reply_markup(
        inline_message_id=str(posted_dish.message_id),
        reply_markup=user_keyboards.dish_keyboard(should_add_favorite=True),
    )


@router.callback_query(F.data == "add_favorite_btn")
async def add_favorite(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    posted_dish = state_data.get("posted_dish")
    dish_id = state_data.get("dish_id")

    user = BotUser.objects.get(tig_id=callback.from_user.id)
    user.favorites.set([dish_id, *user.favorites.all()])
    await callback.answer("Добавлено в избранное")

    await posted_dish.edit_reply_markup(
        inline_message_id=str(posted_dish.message_id),
        reply_markup=user_keyboards.dish_keyboard(should_add_favorite=False),
    )


@router.callback_query(F.data == "remove_favorite_btn")
async def remove_favorite(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    posted_dish = state_data.get("posted_dish")
    dish_id = state_data.get("dish_id")

    user = BotUser.objects.get(tig_id=callback.from_user.id)
    user.favorites.set([*user.favorites.filter(~Q(id=dish_id))])
    await callback.answer("Удалено из избранного")

    await posted_dish.edit_reply_markup(
        inline_message_id=str(posted_dish.message_id),
        reply_markup=user_keyboards.dish_keyboard(should_add_favorite=True),
    )


# @router.message(States.show_recipe)
# async def get_recipe(message: Message, state: FSMContext):
#     # await message.answer("Recept")
#     # await state.set_state(States.show_ingredients)


@router.message(States.show_ingredients)
async def get_ingredients(message: Message, state: FSMContext):
    await message.answer("ingredients")
    await state.clear()

@router.message(Command(commands=["favorites"]))
async def get_favorites(message: Message, state: FSMContext):

    shown_fav = []
    favorite = BotUser.objects.get(tig_id=message.from_user.id).favorites.first()
   
    if favorite:
        shown_fav.append(favorite.pk)
        await state.update_data(fav_to_show=favorite)
        await state.set_state(States.show_favorite)

    else:
        message.answer(text="Список избранного закончился")

    await state.update_data(shown_fav=shown_fav)

    photo = FSInputFile(favorite.image.path)
    posted_fav = await message.answer_photo(
        photo, caption=favorite.name,
        reply_markup=user_keyboards.fav_keyboard(False)
    )
    await state.update_data(posted_fav=posted_fav, dish_id=favorite.pk)


@router.callback_query(F.data == "prev_fav_btn")
@router.callback_query(F.data == "next_fav_btn")
async def prev_fav(callback: CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    shown_fav = state_data.get("shown_fav")
    if not shown_fav:
        shown_fav = []
    posted_dish = state_data.get("posted_fav")
    if callback.data == "prev_fav_btn":
        if shown_fav:
            favorite = BotUser.objects.get(tig_id=callback.from_user.id).favorites.filter(pk=shown_fav[-1]).first()
            state.update_data(shown_fav=shown_fav.pop())
            new_media = InputMediaPhoto(media=BufferedInputFile.from_file(favorite.image.path), caption=favorite.name)
            await posted_dish.edit_media(
                media=new_media,
                inline_message_id=str(posted_dish.message_id),
                reply_markup=user_keyboards.fav_keyboard(False),
            )
            
            await state.update_data(dish_id=favorite.pk)
        else:
            callback.message.answer(text="Попробуйте пролистать в обратную сторону или начните сначала")

    else:
        favorite = BotUser.objects.get(tig_id=callback.from_user.id).favorites.exclude(pk__in=shown_fav).first()
        if favorite:
            state.update_data(shown_fav=shown_fav.append(favorite.pk))
            new_media = InputMediaPhoto(media=BufferedInputFile.from_file(favorite.image.path), caption=favorite.name)
            await posted_dish.edit_media(
                media=new_media,
                inline_message_id=str(posted_dish.message_id),
                reply_markup=user_keyboards.fav_keyboard(False),
            )
            await state.update_data(dish_id=favorite.pk)
        else:
            await callback.message.answer(text="Список избранных закончился", reply_markup=None)








@router.message(States.show_pay)
async def get_pay(message: Message, state: FSMContext):
    await message.answer("pay")

    # await state.set_state(UserStates.choosing_category)
