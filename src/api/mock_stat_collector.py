"""Mock реализация сборщика статистики с тестовыми данными"""

import random
from datetime import datetime, timedelta

from src.api.schemas import (
    ActivityDataPoint,
    DialogPreview,
    OverallStats,
    StatsResponse,
    UserActivity,
)
from src.api.stat_collector import StatsPeriod


class MockStatCollector:
    """Mock реализация сборщика статистики

    Генерирует реалистичные тестовые данные для разработки frontend
    без необходимости подключения к реальной базе данных
    """

    def __init__(self) -> None:
        """Инициализация Mock сборщика"""
        # Seed для воспроизводимости данных
        random.seed(42)

    async def get_stats(self, period: str) -> StatsResponse:
        """Получить mock статистику за указанный период

        Args:
            period: Период сбора статистики ("day", "week", "month")

        Returns:
            StatsResponse с тестовыми данными

        Raises:
            ValueError: Если указан неверный период
        """
        # Валидация периода
        try:
            stats_period = StatsPeriod(period)
        except ValueError as e:
            raise ValueError(f"Invalid period: {period}. Must be one of: day, week, month") from e

        # Генерация данных
        overall = self._generate_overall_stats(stats_period)
        activity_data = self._generate_activity_data(stats_period)
        recent_dialogs = self._generate_recent_dialogs()
        top_users = self._generate_top_users()

        return StatsResponse(
            overall=overall,
            activity_data=activity_data,
            recent_dialogs=recent_dialogs,
            top_users=top_users,
            period=period,
        )

    def _generate_overall_stats(self, period: StatsPeriod) -> OverallStats:
        """Генерация общей статистики

        Args:
            period: Период для генерации данных

        Returns:
            OverallStats с тестовыми метриками
        """
        # Разные значения для разных периодов
        if period == StatsPeriod.DAY:
            total_dialogs = random.randint(40, 60)
            active_users = random.randint(30, 50)
            avg_dialog_length = round(random.uniform(8.0, 15.0), 1)
        elif period == StatsPeriod.WEEK:
            total_dialogs = random.randint(200, 300)
            active_users = random.randint(150, 250)
            avg_dialog_length = round(random.uniform(10.0, 18.0), 1)
        else:  # MONTH
            total_dialogs = random.randint(800, 1200)
            active_users = random.randint(600, 900)
            avg_dialog_length = round(random.uniform(12.0, 20.0), 1)

        return OverallStats(
            total_dialogs=total_dialogs,
            active_users=active_users,
            avg_dialog_length=avg_dialog_length,
        )

    def _generate_activity_data(self, period: StatsPeriod) -> list[ActivityDataPoint]:
        """Генерация данных для графика активности

        Args:
            period: Период для генерации данных

        Returns:
            Список точек данных для графика
        """
        now = datetime.utcnow()
        data_points: list[ActivityDataPoint] = []

        if period == StatsPeriod.DAY:
            # 24 точки (по часам)
            for hour in range(24):
                timestamp = (now - timedelta(hours=23 - hour)).replace(minute=0, second=0, microsecond=0)
                # Имитация дневной активности: меньше ночью, больше днем
                base_activity = 50
                hour_factor = 1.0
                if 0 <= hour < 6:  # Ночь
                    hour_factor = 0.3
                elif 6 <= hour < 9:  # Утро
                    hour_factor = 0.7
                elif 9 <= hour < 18:  # День
                    hour_factor = 1.5
                elif 18 <= hour < 22:  # Вечер
                    hour_factor = 1.8
                else:  # Поздний вечер
                    hour_factor = 0.8

                message_count = int(base_activity * hour_factor * random.uniform(0.8, 1.2))
                data_points.append(
                    ActivityDataPoint(
                        timestamp=timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        message_count=message_count,
                    )
                )

        elif period == StatsPeriod.WEEK:
            # 7 точек (по дням недели)
            for day in range(7):
                timestamp = (now - timedelta(days=6 - day)).replace(hour=12, minute=0, second=0, microsecond=0)
                # Больше активности в будни
                day_of_week = (now - timedelta(days=6 - day)).weekday()
                day_factor = 0.6 if day_of_week >= 5 else 1.0  # Меньше в выходные

                message_count = int(400 * day_factor * random.uniform(0.8, 1.2))
                data_points.append(
                    ActivityDataPoint(
                        timestamp=timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        message_count=message_count,
                    )
                )

        else:  # MONTH
            # 30 точек (по дням месяца)
            for day in range(30):
                timestamp = (now - timedelta(days=29 - day)).replace(hour=12, minute=0, second=0, microsecond=0)
                message_count = random.randint(150, 350)
                data_points.append(
                    ActivityDataPoint(
                        timestamp=timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        message_count=message_count,
                    )
                )

        return data_points

    def _generate_recent_dialogs(self) -> list[DialogPreview]:
        """Генерация списка последних диалогов

        Returns:
            Список из 10 последних диалогов
        """
        sample_messages = [
            "Спасибо за помощь! Очень полезная информация о выборе музыки для вечеринки.",
            "Можешь посоветовать что-то для расслабления после работы?",
            "Отличные рекомендации! Добавил все треки в плейлист.",
            "Привет! Мне нужна музыка для утренней пробежки, что посоветуешь?",
            "Ищу джазовые композиции для романтического ужина. Есть идеи?",
            "Нужны треки для концентрации во время учебы, желательно без слов.",
            "Классная подборка! Можешь еще что-то похожее порекомендовать?",
            "Ищу энергичную музыку для тренировки в зале.",
            "Спасибо! Твои рекомендации всегда в точку!",
            "Мне нужна спокойная музыка для медитации и йоги.",
            "Какая музыка подойдет для road trip на выходных?",
            "Помоги составить плейлист для работы дома.",
            "Ищу что-то новое в жанре инди-рок.",
            "Можешь порекомендовать классическую музыку для новичка?",
            "Нужна фоновая музыка для кафе, что посоветуешь?",
        ]

        dialogs: list[DialogPreview] = []
        now = datetime.utcnow()

        for i in range(10):
            user_id = random.randint(100000000, 999999999)
            last_message = random.choice(sample_messages)
            # Последние диалоги разбросаны по последним часам
            created_at = now - timedelta(hours=i * 2, minutes=random.randint(0, 59))
            message_count = random.randint(5, 25)

            # Обрезаем сообщение до 100 символов
            if len(last_message) > 100:
                last_message = last_message[:97] + "..."

            dialogs.append(
                DialogPreview(
                    user_id=user_id,
                    last_message=last_message,
                    created_at=created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    message_count=message_count,
                )
            )

        return dialogs

    def _generate_top_users(self) -> list[UserActivity]:
        """Генерация топа активных пользователей

        Returns:
            Список из 5 самых активных пользователей
        """
        top_users: list[UserActivity] = []
        now = datetime.utcnow()

        # Генерируем топ 5 с убывающим количеством сообщений
        message_counts = [
            random.randint(80, 100),
            random.randint(60, 79),
            random.randint(40, 59),
            random.randint(30, 39),
            random.randint(20, 29),
        ]

        for count in message_counts:
            user_id = random.randint(100000000, 999999999)
            last_active = now - timedelta(hours=random.randint(0, 24), minutes=random.randint(0, 59))

            top_users.append(
                UserActivity(
                    user_id=user_id,
                    message_count=count,
                    last_active=last_active.strftime("%Y-%m-%dT%H:%M:%SZ"),
                )
            )

        return top_users
