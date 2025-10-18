"""Схемы данных для API дашборда статистики и чата"""

from dataclasses import dataclass


@dataclass
class OverallStats:
    """Общая статистика по диалогам

    Attributes:
        total_dialogs: Общее количество диалогов за период
        active_users: Количество активных пользователей за период
        avg_dialog_length: Средняя длина диалога (количество сообщений)
    """

    total_dialogs: int
    active_users: int
    avg_dialog_length: float


@dataclass
class ActivityDataPoint:
    """Точка данных для графика активности

    Attributes:
        timestamp: Временная метка (ISO 8601 формат)
        message_count: Количество сообщений в этот период
    """

    timestamp: str  # ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
    message_count: int


@dataclass
class DialogPreview:
    """Превью диалога для списка последних диалогов

    Attributes:
        user_id: ID пользователя Telegram
        last_message: Превью последнего сообщения (первые 100 символов)
        created_at: Дата начала диалога (ISO 8601)
        message_count: Количество сообщений в диалоге
    """

    user_id: int
    last_message: str
    created_at: str  # ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
    message_count: int


@dataclass
class UserActivity:
    """Активность пользователя для топа пользователей

    Attributes:
        user_id: ID пользователя Telegram
        message_count: Количество сообщений пользователя за период
        last_active: Дата последней активности (ISO 8601)
    """

    user_id: int
    message_count: int
    last_active: str  # ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ


@dataclass
class StatsResponse:
    """Полный ответ API со статистикой

    Attributes:
        overall: Общая статистика
        activity_data: Данные для графика активности
        recent_dialogs: Список последних диалогов (последние 10)
        top_users: Топ активных пользователей (топ 5)
        period: Период, за который собрана статистика
    """

    overall: OverallStats
    activity_data: list[ActivityDataPoint]
    recent_dialogs: list[DialogPreview]
    top_users: list[UserActivity]
    period: str  # "day" | "week" | "month"


# ==================== Chat API Schemas ====================


@dataclass
class ChatRequest:
    """Запрос на отправку сообщения в чат

    Attributes:
        message: Текст сообщения пользователя
        mode: Режим работы чата ("normal" | "admin")
        session_id: ID сессии веб-пользователя
    """

    message: str
    mode: str
    session_id: str


@dataclass
class ChatResponse:
    """Ответ от API чата

    Attributes:
        message: Ответное сообщение от AI
        sql_query: SQL запрос (только для admin режима)
        session_id: ID сессии
    """

    message: str
    sql_query: str | None
    session_id: str


@dataclass
class SessionResponse:
    """Ответ от endpoint создания сессии

    Attributes:
        session_id: Уникальный ID сессии
    """

    session_id: str


@dataclass
class ClearChatRequest:
    """Запрос на очистку истории чата

    Attributes:
        session_id: ID сессии для очистки
    """

    session_id: str
