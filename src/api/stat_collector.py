"""Интерфейс сборщика статистики для дашборда"""

from enum import Enum
from typing import Protocol

from src.api.schemas import StatsResponse


class StatsPeriod(str, Enum):
    """Период для сбора статистики"""

    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class StatCollectorProtocol(Protocol):
    """Протокол для сборщиков статистики

    Определяет интерфейс для различных реализаций сбора статистики
    (Mock для разработки frontend, Real для работы с реальными данными)
    """

    async def get_stats(self, period: str) -> StatsResponse:
        """Получить статистику за указанный период

        Args:
            period: Период сбора статистики ("day", "week", "month")

        Returns:
            StatsResponse с данными статистики

        Raises:
            ValueError: Если указан неверный период
        """
        ...
