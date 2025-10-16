"""Pytest fixtures for tests"""

from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio

from src.config import Config
from src.database import Database
from src.dialog_manager import DialogManager
from src.message_repository import MessageRepository


@pytest.fixture
def config(monkeypatch: pytest.MonkeyPatch) -> Config:
    """Fixture для конфигурации с мокированными переменными окружения

    Args:
        monkeypatch: Pytest monkeypatch для мока переменных

    Returns:
        Тестовая конфигурация
    """
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token_123")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key_123")
        monkeypatch.setenv("SYSTEM_PROMPT", "You are a test assistant")
        return Config()


@pytest.fixture
def config_with_max_context(monkeypatch: pytest.MonkeyPatch) -> Config:
    """Fixture для конфигурации с MAX_CONTEXT_MESSAGES

    Args:
        monkeypatch: Pytest monkeypatch для мока переменных

    Returns:
        Тестовая конфигурация с MAX_CONTEXT_MESSAGES=2
    """
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token_123")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key_123")
        monkeypatch.setenv("SYSTEM_PROMPT", "You are a test assistant")
        monkeypatch.setenv("MAX_CONTEXT_MESSAGES", "2")
        return Config()


@pytest_asyncio.fixture
async def test_database(monkeypatch: pytest.MonkeyPatch) -> Database:
    """Fixture для in-memory SQLite базы данных

    Args:
        monkeypatch: Pytest monkeypatch

    Returns:
        Database с in-memory SQLite
    """
    # Use shared in-memory database so all connections see the same data
    test_db_url = "sqlite+aiosqlite:///file:test_db?mode=memory&cache=shared"
    monkeypatch.setenv("DATABASE_URL", test_db_url)

    # Need to reload Config after monkeypatch
    from src.config import Config
    test_config = Config()
    db = Database(test_config)

    # Create tables
    async with db.get_connection() as conn:
        # Create users table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                is_deleted BOOLEAN DEFAULT 0 NOT NULL
            )
            """
        )

        # Create messages table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                length INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                is_deleted BOOLEAN DEFAULT 0 NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        # Create index
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_messages_user_deleted_created
            ON messages(user_id, is_deleted, created_at)
            """
        )

    yield db

    # Cleanup: drop tables after test
    async with db.get_connection() as conn:
        await conn.execute("DROP TABLE IF EXISTS messages")
        await conn.execute("DROP TABLE IF EXISTS users")


@pytest_asyncio.fixture
async def message_repository(test_database: Database) -> MessageRepository:
    """Fixture для MessageRepository с тестовой базой данных

    Args:
        test_database: Тестовая база данных

    Returns:
        MessageRepository для тестирования
    """
    return MessageRepository(test_database)


@pytest_asyncio.fixture
async def dialog_manager(config: Config, message_repository: MessageRepository) -> DialogManager:
    """Fixture для DialogManager с тестовой конфигурацией

    Args:
        config: Тестовая конфигурация
        message_repository: Тестовый репозиторий сообщений

    Returns:
        DialogManager для тестирования
    """
    return DialogManager(config, message_repository)


@pytest.fixture
def logger() -> MagicMock:
    """Fixture для мокированного логгера

    Returns:
        Мокированный structlog.BoundLogger
    """
    mock_logger = MagicMock()
    mock_logger.info = MagicMock()
    mock_logger.error = MagicMock()
    return mock_logger
