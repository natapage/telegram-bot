"""FastAPI приложение для API дашборда статистики и чата"""

import structlog
from typing import Annotated

from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware

from src.api.chat_service import ChatService
from src.api.real_stat_collector import RealStatCollector
from src.api.schemas import ChatRequest, ChatResponse, ClearChatRequest, SessionResponse, StatsResponse
from src.api.session_manager import generate_session_id
from src.api.stat_collector import StatsPeriod
from src.api.text_to_sql_service import TextToSQLService
from src.config import Config
from src.database import Database

# Инициализация логгера
_logger = structlog.get_logger()

# Инициализация базы данных и сервисов
_config = Config()
_database = Database(_config)
_stat_collector = RealStatCollector(_database)
_chat_service = ChatService(_config, _database, _logger)
_text_to_sql_service = TextToSQLService(_config, _database, _logger)


def create_app() -> FastAPI:
    """Создать и настроить FastAPI приложение

    Returns:
        Настроенное FastAPI приложение
    """
    app = FastAPI(
        title="Telegram Bot Dashboard API",
        description="API для получения статистики по диалогам Telegram-бота",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Настройка CORS для доступа из frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # В продакшене заменить на конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict[str, str]:
        """Проверка работоспособности API

        Returns:
            Статус работы API
        """
        return {"status": "ok", "service": "dashboard-api"}

    @app.get("/stats", response_model=StatsResponse, tags=["Statistics"])
    async def get_stats(
        period: Annotated[
            str,
            Query(
                description="Период для сбора статистики",
                enum=[p.value for p in StatsPeriod],
            ),
        ] = "day",
    ) -> StatsResponse:
        """Получить статистику по диалогам за указанный период

        Args:
            period: Период сбора статистики (day/week/month)

        Returns:
            StatsResponse со статистикой за период

        Raises:
            HTTPException: 400 если указан неверный период
        """
        return await _stat_collector.get_stats(period)

    @app.post("/api/chat/message", response_model=ChatResponse, tags=["Chat"])
    async def send_chat_message(request: ChatRequest = Body(...)) -> ChatResponse:
        """Отправка сообщения в чат

        Обрабатывает сообщения в двух режимах:
        - normal: обычный чат с LLM
        - admin: text-to-SQL запросы к статистике

        Args:
            request: Запрос с сообщением, режимом и session_id

        Returns:
            Ответ от AI с опциональным SQL запросом

        Raises:
            HTTPException: 500 при ошибках обработки
        """
        if request.mode == "admin":
            return await _text_to_sql_service.process_message(request)
        else:
            return await _chat_service.process_message(request)

    @app.post("/api/chat/clear", tags=["Chat"])
    async def clear_chat(request: ClearChatRequest = Body(...)) -> dict[str, str]:
        """Очистка истории чата

        Args:
            request: Запрос с session_id для очистки

        Returns:
            Подтверждение очистки

        Raises:
            HTTPException: 500 при ошибках очистки
        """
        await _chat_service.clear_chat(request.session_id)
        return {"status": "ok", "message": "Chat history cleared"}

    @app.get("/api/chat/session", response_model=SessionResponse, tags=["Chat"])
    async def get_or_create_session() -> SessionResponse:
        """Получение нового session ID для веб-пользователя

        Returns:
            SessionResponse с уникальным session_id

        Example:
            GET /api/chat/session
            Response: {"session_id": "web_550e8400-e29b-41d4-a716-446655440000"}
        """
        session_id = generate_session_id()
        return SessionResponse(session_id=session_id)

    return app


# Создаем приложение для использования в uvicorn
app = create_app()
