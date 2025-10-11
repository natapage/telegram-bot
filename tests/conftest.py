"""Pytest fixtures for tests"""

from unittest.mock import MagicMock, patch

import pytest

from src.config import Config
from src.dialog_manager import DialogManager


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


@pytest.fixture
def dialog_manager(config: Config) -> DialogManager:
    """Fixture для DialogManager с тестовой конфигурацией

    Args:
        config: Тестовая конфигурация

    Returns:
        DialogManager для тестирования
    """
    return DialogManager(config)


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
