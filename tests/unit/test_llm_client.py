"""Unit tests for LLMClient class"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openai import OpenAIError

from src.config import Config
from src.llm_client import LLMClient


@pytest.fixture
def mock_openai_client() -> AsyncMock:
    """Fixture для мокированного AsyncOpenAI клиента

    Returns:
        Мокированный AsyncOpenAI
    """
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test response"
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.mark.asyncio
async def test_generate_response_returns_content(
    config: Config, logger: MagicMock, mock_openai_client: AsyncMock
) -> None:
    """Тест: успешный вызов generate_response() возвращает корректный ответ"""
    with patch("src.llm_client.AsyncOpenAI", return_value=mock_openai_client):
        client = LLMClient(config, logger)
        messages: list[dict[str, Any]] = [{"role": "user", "content": "Hello"}]

        response = await client.generate_response(messages)

        assert response == "Test response"
        mock_openai_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_generate_response_handles_none_content(
    config: Config, logger: MagicMock, mock_openai_client: AsyncMock
) -> None:
    """Тест: generate_response() возвращает пустую строку если content = None"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = None
    mock_openai_client.chat.completions.create.return_value = mock_response

    with patch("src.llm_client.AsyncOpenAI", return_value=mock_openai_client):
        client = LLMClient(config, logger)
        messages: list[dict[str, Any]] = [{"role": "user", "content": "Hello"}]

        response = await client.generate_response(messages)

        assert response == ""


@pytest.mark.asyncio
async def test_generate_response_logs_request_and_response(
    config: Config, logger: MagicMock, mock_openai_client: AsyncMock
) -> None:
    """Тест: логирование запроса и ответа"""
    with patch("src.llm_client.AsyncOpenAI", return_value=mock_openai_client):
        client = LLMClient(config, logger)
        messages: list[dict[str, Any]] = [{"role": "user", "content": "Hello"}]

        await client.generate_response(messages)

        # Проверяем логирование запроса
        logger.info.assert_any_call("llm_request", model=config.OPENAI_MODEL, message_count=1)
        # Проверяем логирование ответа
        logger.info.assert_any_call("llm_response", length=13)  # len("Test response")


@pytest.mark.asyncio
async def test_generate_response_raises_and_logs_openai_error(
    config: Config, logger: MagicMock, mock_openai_client: AsyncMock
) -> None:
    """Тест: обработка OpenAIError при ошибке API"""
    mock_openai_client.chat.completions.create.side_effect = OpenAIError("API Error")

    with patch("src.llm_client.AsyncOpenAI", return_value=mock_openai_client):
        client = LLMClient(config, logger)
        messages: list[dict[str, Any]] = [{"role": "user", "content": "Hello"}]

        with pytest.raises(OpenAIError):
            await client.generate_response(messages)

        # Проверяем логирование ошибки
        logger.error.assert_called_once()
        call_args = logger.error.call_args
        assert call_args[0][0] == "llm_api_error"
        assert "error" in call_args[1]
        assert call_args[1]["exc_info"] is True


@pytest.mark.asyncio
async def test_generate_response_raises_and_logs_timeout_error(
    config: Config, logger: MagicMock, mock_openai_client: AsyncMock
) -> None:
    """Тест: обработка TimeoutError при таймауте"""
    mock_openai_client.chat.completions.create.side_effect = TimeoutError("Timeout")

    with patch("src.llm_client.AsyncOpenAI", return_value=mock_openai_client):
        client = LLMClient(config, logger)
        messages: list[dict[str, Any]] = [{"role": "user", "content": "Hello"}]

        with pytest.raises(TimeoutError):
            await client.generate_response(messages)

        # Проверяем логирование ошибки
        logger.error.assert_called_once()
        call_args = logger.error.call_args
        assert call_args[0][0] == "llm_timeout_error"
        assert "error" in call_args[1]
        assert call_args[1]["exc_info"] is True


@pytest.mark.asyncio
async def test_generate_response_passes_correct_parameters(
    config: Config, logger: MagicMock, mock_openai_client: AsyncMock
) -> None:
    """Тест: правильные параметры передаются в OpenAI API"""
    with patch("src.llm_client.AsyncOpenAI", return_value=mock_openai_client):
        client = LLMClient(config, logger)
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": "System"},
            {"role": "user", "content": "Hello"},
        ]

        await client.generate_response(messages)

        # Проверяем параметры вызова
        mock_openai_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_openai_client.chat.completions.create.call_args[1]
        assert call_kwargs["model"] == config.OPENAI_MODEL
        assert call_kwargs["messages"] == messages
