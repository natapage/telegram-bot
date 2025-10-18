"""Реальная реализация сборщика статистики из базы данных"""

from datetime import datetime, timedelta

from src.api.schemas import (
    ActivityDataPoint,
    DialogPreview,
    OverallStats,
    StatsResponse,
    UserActivity,
)
from src.api.stat_collector import StatsPeriod
from src.database import Database


class RealStatCollector:
    """Реальная реализация сборщика статистики

    Получает данные из SQLite базы данных с реальными диалогами
    """

    def __init__(self, database: Database) -> None:
        """Инициализация сборщика

        Args:
            database: Менеджер подключений к базе данных
        """
        self.database = database

    async def get_stats(self, period: str) -> StatsResponse:
        """Получить реальную статистику за указанный период

        Args:
            period: Период сбора статистики ("day", "week", "month")

        Returns:
            StatsResponse с реальными данными из БД

        Raises:
            ValueError: Если указан неверный период
        """
        # Валидация периода
        try:
            stats_period = StatsPeriod(period)
        except ValueError as e:
            raise ValueError(f"Invalid period: {period}. Must be one of: day, week, month") from e

        # Вычисляем временной диапазон для фильтрации
        now = datetime.utcnow()
        start_time = self._get_period_start(now, stats_period)

        # Собираем статистику
        overall = await self._get_overall_stats(start_time)
        activity_data = await self._get_activity_data(start_time, stats_period)
        recent_dialogs = await self._get_recent_dialogs()
        top_users = await self._get_top_users(start_time)

        return StatsResponse(
            overall=overall,
            activity_data=activity_data,
            recent_dialogs=recent_dialogs,
            top_users=top_users,
            period=period,
        )

    def _get_period_start(self, now: datetime, period: StatsPeriod) -> datetime:
        """Получить начальную дату для периода

        Args:
            now: Текущая дата/время
            period: Период статистики

        Returns:
            Начальная дата периода
        """
        if period == StatsPeriod.DAY:
            return now - timedelta(days=1)
        elif period == StatsPeriod.WEEK:
            return now - timedelta(weeks=1)
        else:  # MONTH
            return now - timedelta(days=30)

    async def _get_overall_stats(self, start_time: datetime) -> OverallStats:
        """Получить общую статистику

        Args:
            start_time: Начало периода

        Returns:
            OverallStats с метриками из БД
        """
        async with self.database.get_connection() as conn:
            # Подсчет уникальных диалогов (пользователей с сообщениями)
            cursor = await conn.execute(
                """
                SELECT COUNT(DISTINCT user_id) as total_dialogs
                FROM messages
                WHERE created_at >= ? AND is_deleted = 0
                """,
                (start_time.isoformat(),),
            )
            row = await cursor.fetchone()
            total_dialogs = row["total_dialogs"] if row else 0

            # Количество активных пользователей (те, у кого есть сообщения за период)
            active_users = total_dialogs

            # Средняя длина диалога (среднее количество сообщений на пользователя)
            cursor = await conn.execute(
                """
                SELECT AVG(message_count) as avg_length
                FROM (
                    SELECT user_id, COUNT(*) as message_count
                    FROM messages
                    WHERE created_at >= ? AND is_deleted = 0
                    GROUP BY user_id
                )
                """,
                (start_time.isoformat(),),
            )
            row = await cursor.fetchone()
            avg_dialog_length = float(row["avg_length"]) if row and row["avg_length"] else 0.0

        return OverallStats(
            total_dialogs=total_dialogs,
            active_users=active_users,
            avg_dialog_length=round(avg_dialog_length, 1),
        )

    async def _get_activity_data(
        self, start_time: datetime, period: StatsPeriod
    ) -> list[ActivityDataPoint]:
        """Получить данные для графика активности

        Args:
            start_time: Начало периода
            period: Период статистики

        Returns:
            Список точек данных для графика
        """
        async with self.database.get_connection() as conn:
            if period == StatsPeriod.DAY:
                # По часам за последние 24 часа
                data_points = await self._get_hourly_activity(conn, start_time)
            elif period == StatsPeriod.WEEK:
                # По дням за последние 7 дней
                data_points = await self._get_daily_activity(conn, start_time, 7)
            else:  # MONTH
                # По дням за последние 30 дней
                data_points = await self._get_daily_activity(conn, start_time, 30)

        return data_points

    async def _get_hourly_activity(self, conn, start_time: datetime) -> list[ActivityDataPoint]:
        """Получить активность по часам

        Args:
            conn: Соединение с БД
            start_time: Начало периода

        Returns:
            Список точек данных по часам
        """
        cursor = await conn.execute(
            """
            SELECT
                strftime('%Y-%m-%d %H:00:00', created_at) as hour,
                COUNT(*) as message_count
            FROM messages
            WHERE created_at >= ? AND is_deleted = 0
            GROUP BY hour
            ORDER BY hour ASC
            """,
            (start_time.isoformat(),),
        )
        rows = await cursor.fetchall()

        # Создаем словарь для быстрого поиска
        data_dict = {row["hour"]: row["message_count"] for row in rows}

        # Генерируем все 24 часа с данными или нулями
        now = datetime.utcnow()
        data_points: list[ActivityDataPoint] = []

        for hour in range(24):
            timestamp = (now - timedelta(hours=23 - hour)).replace(minute=0, second=0, microsecond=0)
            hour_key = timestamp.strftime("%Y-%m-%d %H:00:00")
            message_count = data_dict.get(hour_key, 0)

            data_points.append(
                ActivityDataPoint(
                    timestamp=timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    message_count=message_count,
                )
            )

        return data_points

    async def _get_daily_activity(
        self, conn, start_time: datetime, num_days: int
    ) -> list[ActivityDataPoint]:
        """Получить активность по дням

        Args:
            conn: Соединение с БД
            start_time: Начало периода
            num_days: Количество дней

        Returns:
            Список точек данных по дням
        """
        cursor = await conn.execute(
            """
            SELECT
                DATE(created_at) as date,
                COUNT(*) as message_count
            FROM messages
            WHERE created_at >= ? AND is_deleted = 0
            GROUP BY date
            ORDER BY date ASC
            """,
            (start_time.isoformat(),),
        )
        rows = await cursor.fetchall()

        # Создаем словарь для быстрого поиска
        data_dict = {row["date"]: row["message_count"] for row in rows}

        # Генерируем все дни с данными или нулями
        now = datetime.utcnow()
        data_points: list[ActivityDataPoint] = []

        for day in range(num_days):
            timestamp = (now - timedelta(days=num_days - 1 - day)).replace(
                hour=12, minute=0, second=0, microsecond=0
            )
            date_key = timestamp.strftime("%Y-%m-%d")
            message_count = data_dict.get(date_key, 0)

            data_points.append(
                ActivityDataPoint(
                    timestamp=timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    message_count=message_count,
                )
            )

        return data_points

    async def _get_recent_dialogs(self) -> list[DialogPreview]:
        """Получить список последних диалогов

        Returns:
            Список из 10 последних диалогов
        """
        async with self.database.get_connection() as conn:
            cursor = await conn.execute(
                """
                SELECT
                    user_id,
                    COUNT(*) as message_count,
                    MAX(created_at) as last_message_time,
                    MIN(created_at) as created_at,
                    (
                        SELECT content
                        FROM messages m2
                        WHERE m2.user_id = m1.user_id
                          AND m2.is_deleted = 0
                        ORDER BY m2.created_at DESC
                        LIMIT 1
                    ) as last_message
                FROM messages m1
                WHERE is_deleted = 0
                GROUP BY user_id
                ORDER BY last_message_time DESC
                LIMIT 10
                """
            )
            rows = await cursor.fetchall()

        dialogs: list[DialogPreview] = []
        for row in rows:
            last_message = row["last_message"] or ""
            # Обрезаем сообщение до 100 символов
            if len(last_message) > 100:
                last_message = last_message[:97] + "..."

            dialogs.append(
                DialogPreview(
                    user_id=row["user_id"],
                    last_message=last_message,
                    created_at=row["created_at"],
                    message_count=row["message_count"],
                )
            )

        return dialogs

    async def _get_top_users(self, start_time: datetime) -> list[UserActivity]:
        """Получить топ активных пользователей

        Args:
            start_time: Начало периода

        Returns:
            Список из 5 самых активных пользователей
        """
        async with self.database.get_connection() as conn:
            cursor = await conn.execute(
                """
                SELECT
                    user_id,
                    COUNT(*) as message_count,
                    MAX(created_at) as last_active
                FROM messages
                WHERE created_at >= ? AND is_deleted = 0
                GROUP BY user_id
                ORDER BY message_count DESC
                LIMIT 5
                """,
                (start_time.isoformat(),),
            )
            rows = await cursor.fetchall()

        top_users: list[UserActivity] = []
        for row in rows:
            top_users.append(
                UserActivity(
                    user_id=row["user_id"],
                    message_count=row["message_count"],
                    last_active=row["last_active"],
                )
            )

        return top_users
