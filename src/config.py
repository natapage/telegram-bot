"""Конфигурация приложения из .env файла"""

import os

from dotenv import load_dotenv


class Config:
    """Конфигурация приложения из .env файла"""

    def __init__(self) -> None:
        """Инициализация и загрузка конфигурации

        Raises:
            ValueError: Если отсутствует обязательный параметр
        """
        load_dotenv()

        # Telegram Bot
        self.TELEGRAM_BOT_TOKEN: str = self._get_required("TELEGRAM_BOT_TOKEN")

        # Openrouter/LLM
        self.OPENAI_API_KEY: str = self._get_required("OPENAI_API_KEY")
        self.OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
        self.OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "openai/gpt-4")
        self.SYSTEM_PROMPT: str = self._load_system_prompt()

        # Bot роль
        self.BOT_ROLE_NAME: str = os.getenv("BOT_ROLE_NAME", "ИИ-ассистент")
        self.BOT_ROLE_DESCRIPTION: str = os.getenv("BOT_ROLE_DESCRIPTION", "Помогаю отвечать на вопросы")

        # Логирование
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "logs/")

        # Контекст
        max_context = os.getenv("MAX_CONTEXT_MESSAGES", "0")
        self.MAX_CONTEXT_MESSAGES: int = int(max_context)

        # База данных
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./telegram_bot.db")

    def _get_required(self, key: str) -> str:
        """Получить обязательный параметр из окружения

        Args:
            key: Название переменной окружения

        Returns:
            Значение переменной

        Raises:
            ValueError: Если переменная не установлена
        """
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Обязательная переменная окружения {key} не установлена")
        return value

    def _load_system_prompt(self) -> str:
        """Загрузить системный промпт из файла или переменной окружения

        Returns:
            Текст системного промпта

        Raises:
            ValueError: Если промпт не настроен
        """
        # Попытка загрузить из файла
        prompt_file = os.getenv("SYSTEM_PROMPT_FILE")
        if prompt_file:
            try:
                with open(prompt_file, encoding="utf-8") as f:
                    return f.read().strip()
            except FileNotFoundError as err:
                raise ValueError(f"Файл системного промпта не найден: {prompt_file}") from err

        # Fallback на переменную окружения
        prompt = os.getenv("SYSTEM_PROMPT")
        if prompt:
            return prompt

        # Если ничего не настроено
        raise ValueError("Системный промпт не настроен. Укажите SYSTEM_PROMPT_FILE или SYSTEM_PROMPT")
