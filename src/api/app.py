"""FastAPI приложение для API дашборда статистики"""

from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.api.mock_stat_collector import MockStatCollector
from src.api.schemas import StatsResponse
from src.api.stat_collector import StatsPeriod

# Глобальный экземпляр коллектора статистики
# В будущем будет заменен на DI container
_stat_collector = MockStatCollector()


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

    return app


# Создаем приложение для использования в uvicorn
app = create_app()
