import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, LabeledPrice, Message, FSInputFile
from aiogram.types.message import ContentType

from bot.config_data.config import load_config
from bot.handlers.states import States
from bot.keyboards import user_keyboards
from bot.models import Dish, Bot_user
from datetime import datetime


router = Router()
config = load_config()
admin_ids = config.admins.ids


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    dish = Dish.objects.all()
    dish_image = FSInputFile(str(dish[0].image))
    ingredients = dish[0].ingridients.all()
    await message.answer(
        text="Рецепт дня",
        reply_markup=user_keyboards.start_keyboard(),
    )
    await config.bot.send_photo(chat_id=message.chat.id, photo=dish_image)
    for ingredient in ingredients:
        await message.answer(
            text=f'{str(ingredient.name)} {ingredient.price} RUB {ingredient.count}'
        )
    user_id = int(message.from_user.id)
    await state.update_data(prods=[])
    await state.update_data(user_id=user_id)
    await state.set_state(States.choosing_category)
    await state.set_state(States.show_subscription)


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


@router.message(States.show_subscription)
@router.message(F.text.lower() == "Подписаться")
async def chose_subscriptions(message: Message, state: FSMContext):
    await message.answer(
        text='Подписка на выбор',
        reply_markup=user_keyboards.chose_subscription()
    )
    await state.set_state(States.show_subscription_1_week)


@router.callback_query(F.data == 'week')
@router.message(States.show_subscription_1_week)
async def get_subscription_week(callback: CallbackQuery, state: FSMContext):
    PRICE = LabeledPrice(label='Неделя', amount=29900)
    if config.payment.split(':')[1] == 'TEST':
        await callback.message.answer(
            text="Оплатить подписку",
        )
    await state.set_state(States.show_pay)
    await config.bot.send_invoice(
        callback.message.chat.id,
        title="Подписка на бота",
        description="Активация подписки на неделю",
        provider_token=config.payment,
        currency='rub',
        # photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        # photo_height=512,  # !=0/None, иначе изображение не покажется
        # photo_width=512,
        # photo_size=512,
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=[PRICE],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use'
    )


@router.callback_query(F.data == 'month')
@router.message(States.show_subscription_1_week)
async def get_subscription_month(callback: CallbackQuery, state: FSMContext):
    PRICE = LabeledPrice(label='Месяц', amount=79900)
    if config.payment.split(':')[1] == 'TEST':
        await callback.message.answer(
            text="Оплатить подписку",
        )
    await state.set_state(States.show_pay)
    await config.bot.send_invoice(
        callback.message.chat.id,
        title="Подписка на бота",
        description="Активация подписки на 1 месяц",
        provider_token=config.payment,
        currency='rub',
        # photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        # photo_height=512,  # !=0/None, иначе изображение не покажется
        # photo_width=512,
        # photo_size=512,
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=[PRICE],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use'
    )


@router.message(States.show_pay)
@router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    await config.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(States.show_successful_payment)
    

@router.message(States.show_successful_payment)
@router.message(Command(commands=[ContentType.SUCCESSFUL_PAYMENT]))
async def on_successful_payment(message: Message, state: FSMContext):
    current_datetime = datetime.now()
    users = Bot_user.objects.create(
        name=message.from_user.first_name,
        tig_id=message.from_user.id,
        subscription_date=current_datetime
        )
    await message.answer(f"""Оплата успешно проведена! {users.name} вы получили премиум-подписку на сумму 
{message.successful_payment.total_amount // 100} {message.successful_payment.currency}.""")
