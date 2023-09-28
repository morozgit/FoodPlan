from django.core.management.base import BaseCommand
from django.conf import settings
import logging
import asyncio
from bot.config_data.config import load_config
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import user_handlers

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            asyncio.run(self.start_bot())
        except (KeyboardInterrupt, SystemExit):
            logger.error("Bot stopped")

    async def start_bot(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(filename)s:%(lineno)d | %(levelname)-8s | [%(asctime)s] | "
            "%(name)s | %(message)s",
        )
        logger.info("Starting bot")
        config = load_config()

        bot = Bot(config.telegram_bot.token, parse_mode="HTML")
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(user_handlers.router)

        dp.startup.register(self.set_main_menu)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    async def set_main_menu(self, bot: Bot):
        await bot.set_my_commands(
            [
                types.BotCommand(command="/help", description="Справка по работе бота"),
                types.BotCommand(command="/support", description="Поддержка"),
            ]
        )
