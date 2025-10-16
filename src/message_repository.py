"""Репозиторий для работы с сообщениями в базе данных"""

from typing import Any

from src.database import Database


class MessageRepository:
    """Репозиторий для операций с сообщениями"""

    def __init__(self, database: Database) -> None:
        """Инициализация репозитория

        Args:
            database: Менеджер подключений к базе данных
        """
        self.database = database

    async def create_user(self, user_id: int) -> None:
        """Создать пользователя, если не существует

        Args:
            user_id: ID пользователя Telegram
        """
        async with self.database.get_connection() as conn:
            await conn.execute(
                """
                INSERT OR IGNORE INTO users (id, created_at, is_deleted)
                VALUES (?, CURRENT_TIMESTAMP, 0)
                """,
                (user_id,),
            )

    async def get_user_messages(self, user_id: int) -> list[dict[str, Any]]:
        """Получить все не удаленные сообщения пользователя

        Args:
            user_id: ID пользователя Telegram

        Returns:
            Список сообщений в формате словарей
        """
        async with self.database.get_connection() as conn:
            cursor = await conn.execute(
                """
                SELECT id, user_id, role, content, length, created_at, is_deleted
                FROM messages
                WHERE user_id = ? AND is_deleted = 0
                ORDER BY created_at ASC
                """,
                (user_id,),
            )
            rows = await cursor.fetchall()
            # Convert Row objects to dicts
            return [dict(row) for row in rows]

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        """Добавить сообщение в историю

        Args:
            user_id: ID пользователя Telegram
            role: Роль отправителя (user/assistant/system)
            content: Текст сообщения
        """
        # Ensure user exists
        await self.create_user(user_id)

        # Calculate message length
        length = len(content)

        async with self.database.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO messages (user_id, role, content, length, created_at, is_deleted)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 0)
                """,
                (user_id, role, content, length),
            )

    async def soft_delete_user_messages(self, user_id: int) -> None:
        """Мягкое удаление всех сообщений пользователя

        Args:
            user_id: ID пользователя Telegram
        """
        async with self.database.get_connection() as conn:
            await conn.execute(
                """
                UPDATE messages
                SET is_deleted = 1
                WHERE user_id = ? AND is_deleted = 0
                """,
                (user_id,),
            )

