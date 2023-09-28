import asyncio

from FoodPlan.settings import TELEGRAM_TOKEN
from aiogram import Bot, Dispatcher
from django.core.management.base import BaseCommand

from bot import handlers

telegram_bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher()


async def main():
    dispatcher.include_router(handlers.router)
    await dispatcher.start_polling(telegram_bot)


class Command(BaseCommand):
    help = 'Telegram bot commands'  # todo

    def handle(self, *args, **options):
        asyncio.run(main())
