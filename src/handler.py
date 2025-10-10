"""Обработчики сообщений Telegram"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


class MessageHandler:
    """Обработчики сообщений Telegram"""

    def __init__(self) -> None:
        """Инициализация роутера и регистрация обработчиков"""
        self.router: Router = Router()
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Регистрация всех обработчиков"""
        self.router.message.register(self.handle_start, Command("start"))
        self.router.message.register(self.handle_text)

    async def handle_start(self, message: Message) -> None:
        """Обработчик команды /start

        Args:
            message: Входящее сообщение
        """
        await message.answer("Привет! Я LLM-ассистент")

    async def handle_text(self, message: Message) -> None:
        """Обработчик текстовых сообщений

        Args:
            message: Входящее сообщение
        """
        username = message.from_user.username or message.from_user.first_name or "User"
        await message.answer(f"Hello, {username}!")
