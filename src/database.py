"""Управление соединением с базой данных SQLite"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aiosqlite

from src.config import Config


class Database:
    """Менеджер подключений к базе данных"""

    def __init__(self, config: Config) -> None:
        """Инициализация менеджера базы данных

        Args:
            config: Конфигурация приложения
        """
        self.config = config
        # Extract SQLite file path from DATABASE_URL
        # Format: sqlite+aiosqlite:///./telegram_bot.db or sqlite+aiosqlite:///file:...
        db_url = config.DATABASE_URL
        self.db_path = db_url.replace("sqlite+aiosqlite:///", "")
        # Handle special URI formats (e.g., file:test_db?mode=memory&cache=shared)
        # Regular file path - ensure it starts with ./
        if (
            not self.db_path.startswith("file:")
            and not self.db_path.startswith("./")
            and not self.db_path.startswith("/")
        ):
            self.db_path = "./" + self.db_path

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[aiosqlite.Connection]:
        """Получить async соединение с базой данных

        Yields:
            aiosqlite.Connection: Соединение с базой данных
        """
        conn = await aiosqlite.connect(self.db_path)
        # Enable foreign keys support
        await conn.execute("PRAGMA foreign_keys = ON")
        # Set row factory to dict for easier data access
        conn.row_factory = aiosqlite.Row
        try:
            yield conn
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.close()
