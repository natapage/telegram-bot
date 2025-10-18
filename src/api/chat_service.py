"""Сервис для обработки чата (normal mode)"""

import structlog

from src.api.schemas import ChatRequest, ChatResponse
from src.api.session_manager import session_id_to_user_id
from src.config import Config
from src.database import Database
from src.dialog_manager import DialogManager
from src.llm_client import LLMClient
from src.message_repository import MessageRepository


class ChatService:
    """Сервис для обработки запросов чата в normal режиме"""

    def __init__(self, config: Config, database: Database, logger: structlog.BoundLogger) -> None:
        """Инициализация сервиса чата

        Args:
            config: Конфигурация приложения
            database: Менеджер подключений к базе данных
            logger: Логгер приложения
        """
        self.config = config
        self.database = database
        self.logger = logger
        self.llm_client = LLMClient(config, logger)
        self.repository = MessageRepository(database)
        self.dialog_manager = DialogManager(config, self.repository)

    async def process_message(self, request: ChatRequest) -> ChatResponse:
        """Обработка сообщения в normal режиме

        Логика:
        1. Конвертировать session_id в user_id для БД
        2. Добавить сообщение пользователя в историю
        3. Получить полную историю диалога
        4. Отправить в LLM для генерации ответа
        5. Сохранить ответ ассистента в историю
        6. Вернуть ответ

        Args:
            request: Запрос от пользователя

        Returns:
            Ответ с сообщением от AI

        Raises:
            Exception: При ошибках LLM или БД
        """
        # Конвертация session_id в user_id
        user_id = session_id_to_user_id(request.session_id)

        self.logger.info(
            "chat_message_received",
            session_id=request.session_id,
            user_id=user_id,
            mode=request.mode,
            message_length=len(request.message),
        )

        try:
            # Добавить сообщение пользователя в историю
            await self.dialog_manager.add_message(user_id, "user", request.message)

            # Получить полную историю диалога
            history = await self.dialog_manager.get_history(user_id)

            # Генерация ответа от LLM
            response_text = await self.llm_client.generate_response(history)

            # Сохранить ответ ассистента в историю
            await self.dialog_manager.add_message(user_id, "assistant", response_text)

            self.logger.info(
                "chat_response_generated",
                session_id=request.session_id,
                user_id=user_id,
                response_length=len(response_text),
            )

            return ChatResponse(message=response_text, sql_query=None, session_id=request.session_id)

        except Exception as e:
            self.logger.error(
                "chat_processing_error", session_id=request.session_id, user_id=user_id, error=str(e), exc_info=True
            )
            raise

    async def clear_chat(self, session_id: str) -> None:
        """Очистка истории чата для сессии

        Args:
            session_id: ID сессии для очистки
        """
        user_id = session_id_to_user_id(session_id)

        self.logger.info("chat_clear_requested", session_id=session_id, user_id=user_id)

        try:
            await self.dialog_manager.clear_history(user_id)
            self.logger.info("chat_cleared", session_id=session_id, user_id=user_id)
        except Exception as e:
            self.logger.error("chat_clear_error", session_id=session_id, user_id=user_id, error=str(e), exc_info=True)
            raise
