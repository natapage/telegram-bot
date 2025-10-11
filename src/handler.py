"""Обработчики сообщений Telegram"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.llm_client import LLMClient
from src.dialog_manager import DialogManager


class MessageHandler:
    """Обработчики сообщений Telegram"""

    def __init__(self, llm_client: LLMClient, dialog_manager: DialogManager) -> None:
        """Инициализация роутера и регистрация обработчиков

        Args:
            llm_client: Клиент для работы с LLM
            dialog_manager: Менеджер истории диалогов
        """
        self.llm_client: LLMClient = llm_client
        self.dialog_manager: DialogManager = dialog_manager
        self.router: Router = Router()
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Регистрация всех обработчиков"""
        self.router.message.register(self.handle_start, Command("start"))
        self.router.message.register(self.handle_clear, Command("clear"))
        self.router.message.register(self.handle_text)

    async def handle_start(self, message: Message) -> None:
        """Обработчик команды /start

        Args:
            message: Входящее сообщение
        """
        await message.answer("Привет! Я LLM-ассистент")

    async def handle_clear(self, message: Message) -> None:
        """Обработчик команды /clear

        Args:
            message: Входящее сообщение
        """
        user_id = message.from_user.id
        self.dialog_manager.clear_history(user_id)
        await message.answer("История диалога очищена")

    async def handle_text(self, message: Message) -> None:
        """Обработчик текстовых сообщений

        Args:
            message: Входящее сообщение
        """
        user_id = message.from_user.id

        # Добавить сообщение пользователя в историю
        self.dialog_manager.add_message(user_id, "user", message.text)

        # Получить полную историю и отправить в LLM
        history = self.dialog_manager.get_history(user_id)
        response = await self.llm_client.generate_response(history)

        # Добавить ответ ассистента в историю
        self.dialog_manager.add_message(user_id, "assistant", response)

        await message.answer(response)
