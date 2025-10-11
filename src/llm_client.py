"""Клиент для работы с LLM через OpenAI API"""
import structlog
from openai import AsyncOpenAI
from src.config import Config


class LLMClient:
    """Клиент для работы с LLM через OpenAI API"""

    def __init__(self, config: Config, logger: structlog.BoundLogger) -> None:
        """Инициализация клиента OpenAI

        Args:
            config: Конфигурация приложения
            logger: Логгер приложения
        """
        self.config: Config = config
        self.logger: structlog.BoundLogger = logger
        self.client: AsyncOpenAI = AsyncOpenAI(
            base_url=config.OPENAI_BASE_URL,
            api_key=config.OPENAI_API_KEY
        )

    async def generate_response(self, messages: list[dict]) -> str:
        """Генерация ответа от LLM

        Args:
            messages: История сообщений в формате OpenAI API

        Returns:
            Ответ от LLM
        """
        # Логирование запроса
        self.logger.info("llm_request", model=self.config.OPENAI_MODEL, message_count=len(messages))

        response = await self.client.chat.completions.create(
            model=self.config.OPENAI_MODEL,
            messages=messages
        )

        content = response.choices[0].message.content

        # Логирование ответа
        self.logger.info("llm_response", length=len(content))

        return content
