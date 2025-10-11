"""Telegram Bot с инициализацией aiogram"""

from aiogram import Bot as AiogramBot
from aiogram import Dispatcher

from src.config import Config


class Bot:
    """Telegram Bot с инициализацией aiogram"""

    def __init__(self, config: Config) -> None:
        """Инициализация бота и диспетчера

        Args:
            config: Конфигурация приложения
        """
        self.config: Config = config
        self.bot: AiogramBot = AiogramBot(token=config.TELEGRAM_BOT_TOKEN)
        self.dp: Dispatcher = Dispatcher()

    async def start(self) -> None:
        """Запуск polling бота"""
        await self.dp.start_polling(self.bot)
