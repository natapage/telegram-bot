"""Клиент для работы с LLM через OpenAI API"""

from typing import Any

import structlog
from openai import AsyncOpenAI, OpenAIError

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
        self.client: AsyncOpenAI = AsyncOpenAI(base_url=config.OPENAI_BASE_URL, api_key=config.OPENAI_API_KEY)

    async def generate_response(self, messages: list[dict[str, Any]]) -> str:
        """Генерация ответа от LLM

        Args:
            messages: История сообщений в формате OpenAI API

        Returns:
            Ответ от LLM

        Raises:
            OpenAIError: При ошибках API (неверный ключ, лимиты и т.д.)
            TimeoutError: При таймауте запроса
        """
        # Логирование запроса
        self.logger.info("llm_request", model=self.config.OPENAI_MODEL, message_count=len(messages))

        try:
            response = await self.client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=messages,  # type: ignore[arg-type]
            )
        except OpenAIError as e:
            self.logger.error("llm_api_error", error=str(e), exc_info=True)
            raise
        except TimeoutError as e:
            self.logger.error("llm_timeout_error", error=str(e), exc_info=True)
            raise

        content = response.choices[0].message.content

        # Логирование ответа
        self.logger.info("llm_response", length=len(content) if content else 0)

        return content or ""
