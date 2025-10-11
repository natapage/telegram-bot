"""Клиент для работы с LLM через OpenAI API"""
from openai import AsyncOpenAI
from src.config import Config


class LLMClient:
    """Клиент для работы с LLM через OpenAI API"""

    def __init__(self, config: Config) -> None:
        """Инициализация клиента OpenAI

        Args:
            config: Конфигурация приложения
        """
        self.config: Config = config
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
        response = await self.client.chat.completions.create(
            model=self.config.OPENAI_MODEL,
            messages=messages
        )

        return response.choices[0].message.content
