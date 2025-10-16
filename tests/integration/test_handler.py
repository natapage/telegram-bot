"""Integration tests for MessageHandler"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.config import Config
from src.dialog_manager import DialogManager
from src.handler import MessageHandler
from src.llm_client import LLMClient


@pytest.fixture
def mock_llm_client(config: Config) -> LLMClient:
    """Fixture для мокированного LLMClient

    Args:
        config: Тестовая конфигурация

    Returns:
        Мокированный LLMClient
    """
    mock_client = MagicMock(spec=LLMClient)
    mock_client.generate_response = AsyncMock(return_value="Test response")
    return mock_client


@pytest.fixture
def message_handler(mock_llm_client: LLMClient, dialog_manager: DialogManager, logger: MagicMock) -> MessageHandler:
    """Fixture для MessageHandler с мокированными зависимостями

    Args:
        mock_llm_client: Мокированный LLM клиент
        dialog_manager: Менеджер диалогов
        logger: Мокированный логгер

    Returns:
        MessageHandler для тестирования
    """
    return MessageHandler(mock_llm_client, dialog_manager, logger)


@pytest.mark.asyncio
async def test_role_command_sends_bot_role_info(message_handler: MessageHandler, config: Config) -> None:
    """Тест: команда /role отправляет информацию о роли бота"""
    # Создаем мокированное сообщение
    message = AsyncMock()
    message.answer = AsyncMock()

    # Вызываем обработчик
    await message_handler.handle_role(message)

    # Проверяем что answer был вызван
    message.answer.assert_called_once()

    # Получаем текст ответа
    response_text = message.answer.call_args[0][0]

    # Проверяем что ответ не пустой
    assert len(response_text) > 0


@pytest.mark.asyncio
async def test_role_command_includes_role_name(message_handler: MessageHandler, config: Config) -> None:
    """Тест: ответ команды /role содержит название роли"""
    # Создаем мокированное сообщение
    message = AsyncMock()
    message.answer = AsyncMock()

    # Вызываем обработчик
    await message_handler.handle_role(message)

    # Получаем текст ответа
    response_text = message.answer.call_args[0][0]

    # Проверяем что ответ содержит название роли
    assert config.BOT_ROLE_NAME in response_text


@pytest.mark.asyncio
async def test_role_command_includes_role_description(message_handler: MessageHandler, config: Config) -> None:
    """Тест: ответ команды /role содержит описание роли"""
    # Создаем мокированное сообщение
    message = AsyncMock()
    message.answer = AsyncMock()

    # Вызываем обработчик
    await message_handler.handle_role(message)

    # Получаем текст ответа
    response_text = message.answer.call_args[0][0]

    # Проверяем что ответ содержит описание роли
    assert config.BOT_ROLE_DESCRIPTION in response_text
