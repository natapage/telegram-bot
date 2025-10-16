"""Управление историей диалогов с персистентным хранением"""

from typing import Any

from src.config import Config
from src.message_repository import MessageRepository


class DialogManager:
    """Управление историей диалогов с персистентным хранением"""

    def __init__(self, config: Config, repository: MessageRepository) -> None:
        """Инициализация менеджера диалогов

        Args:
            config: Конфигурация приложения
            repository: Репозиторий для работы с сообщениями
        """
        self.config: Config = config
        self.repository: MessageRepository = repository

    async def get_history(self, user_id: int) -> list[dict[str, Any]]:
        """Получить историю диалога пользователя

        Args:
            user_id: ID пользователя

        Returns:
            Список сообщений в формате OpenAI API
        """
        # Загрузить сообщения из базы данных
        messages = await self.repository.get_user_messages(user_id)

        # Преобразовать формат БД в формат OpenAI API
        history = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        # Добавить системный промпт в начало (не хранится в БД)
        history = [{"role": "system", "content": self.config.SYSTEM_PROMPT}] + history

        # Применить обрезку контекста если настроено
        if self.config.MAX_CONTEXT_MESSAGES > 0:
            history = self._trim_history(history)

        return history

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        """Добавить сообщение в историю

        Args:
            user_id: ID пользователя
            role: Роль отправителя (user/assistant)
            content: Текст сообщения
        """
        await self.repository.add_message(user_id, role, content)

    async def clear_history(self, user_id: int) -> None:
        """Очистить историю диалога пользователя (мягкое удаление)

        Args:
            user_id: ID пользователя
        """
        await self.repository.soft_delete_user_messages(user_id)

    def _trim_history(self, history: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Обрезать историю до MAX_CONTEXT_MESSAGES

        Сохраняет системный промпт + последние N*2 сообщений (пары user+assistant)

        Args:
            history: Полная история диалога

        Returns:
            Обрезанная история
        """
        max_messages = self.config.MAX_CONTEXT_MESSAGES

        if max_messages <= 0 or len(history) <= 1:
            return history

        # Системный промпт (первое сообщение)
        system_prompt = [history[0]] if history and history[0]["role"] == "system" else []

        # Диалоговые сообщения (без системного промпта)
        dialog_messages = history[1:] if system_prompt else history

        # Оставить последние N*2 сообщений (пары user+assistant)
        max_dialog_messages = max_messages * 2

        if len(dialog_messages) > max_dialog_messages:
            dialog_messages = dialog_messages[-max_dialog_messages:]

        return system_prompt + dialog_messages
