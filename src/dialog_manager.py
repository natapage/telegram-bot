"""Управление историей диалогов в памяти"""
from src.config import Config


class DialogManager:
    """Управление историей диалогов в памяти"""

    def __init__(self, config: Config) -> None:
        """Инициализация менеджера диалогов

        Args:
            config: Конфигурация приложения
        """
        self.config: Config = config
        self.dialogs: dict[int, list[dict]] = {}

    def get_history(self, user_id: int) -> list[dict]:
        """Получить историю диалога пользователя

        Args:
            user_id: ID пользователя

        Returns:
            Список сообщений в формате OpenAI API
        """
        if user_id not in self.dialogs:
            # Инициализация с системным промптом
            self.dialogs[user_id] = [
                {"role": "system", "content": self.config.SYSTEM_PROMPT}
            ]
        return self.dialogs[user_id]

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
