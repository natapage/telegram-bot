"""Управление историей диалогов в памяти"""

from typing import Any

from src.config import Config


class DialogManager:
    """Управление историей диалогов в памяти"""

    def __init__(self, config: Config) -> None:
        """Инициализация менеджера диалогов

        Args:
            config: Конфигурация приложения
        """
        self.config: Config = config
        self.dialogs: dict[int, list[dict[str, Any]]] = {}

    def get_history(self, user_id: int) -> list[dict[str, Any]]:
        """Получить историю диалога пользователя

        Args:
            user_id: ID пользователя

        Returns:
            Список сообщений в формате OpenAI API
        """
        if user_id not in self.dialogs:
            # Инициализация с системным промптом
            self.dialogs[user_id] = [{"role": "system", "content": self.config.SYSTEM_PROMPT}]

        history = self.dialogs[user_id]

        # Применить обрезку контекста если настроено
        if self.config.MAX_CONTEXT_MESSAGES > 0:
            history = self._trim_history(history)
            self.dialogs[user_id] = history

        return history

    def add_message(self, user_id: int, role: str, content: str) -> None:
        """Добавить сообщение в историю

        Args:
            user_id: ID пользователя
            role: Роль отправителя (user/assistant)
            content: Текст сообщения
        """
        history = self.get_history(user_id)
        history.append({"role": role, "content": content})

    def clear_history(self, user_id: int) -> None:
        """Очистить историю диалога пользователя

        Args:
            user_id: ID пользователя
        """
        if user_id in self.dialogs:
            del self.dialogs[user_id]

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
