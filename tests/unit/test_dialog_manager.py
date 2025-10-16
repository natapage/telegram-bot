"""Unit tests for DialogManager class"""

from typing import Any

import pytest

from src.config import Config
from src.dialog_manager import DialogManager
from src.message_repository import MessageRepository


@pytest.mark.asyncio
async def test_get_history_creates_new_history_with_system_prompt(
    dialog_manager: DialogManager, config: Config
) -> None:
    """Тест: get_history() создаёт новую историю с системным промптом"""
    user_id = 12345

    history = await dialog_manager.get_history(user_id)

    assert len(history) == 1
    assert history[0]["role"] == "system"
    assert history[0]["content"] == config.SYSTEM_PROMPT


@pytest.mark.asyncio
async def test_get_history_returns_existing_history(dialog_manager: DialogManager) -> None:
    """Тест: get_history() возвращает существующую историю из БД"""
    user_id = 12345

    # Add a message
    await dialog_manager.add_message(user_id, "user", "Hello")

    # Get history twice - should have same content (from DB)
    history1 = await dialog_manager.get_history(user_id)
    history2 = await dialog_manager.get_history(user_id)

    assert len(history1) == len(history2)
    assert history1[1]["content"] == history2[1]["content"]


@pytest.mark.asyncio
async def test_add_message_appends_to_history(dialog_manager: DialogManager) -> None:
    """Тест: add_message() добавляет сообщение в историю"""
    user_id = 12345

    await dialog_manager.add_message(user_id, "user", "Hello")
    history = await dialog_manager.get_history(user_id)

    assert len(history) == 2  # system + user
    assert history[1]["role"] == "user"
    assert history[1]["content"] == "Hello"


@pytest.mark.asyncio
async def test_add_message_preserves_order(dialog_manager: DialogManager) -> None:
    """Тест: add_message() сохраняет порядок сообщений"""
    user_id = 12345

    await dialog_manager.add_message(user_id, "user", "First")
    await dialog_manager.add_message(user_id, "assistant", "Second")
    await dialog_manager.add_message(user_id, "user", "Third")

    history = await dialog_manager.get_history(user_id)

    assert len(history) == 4  # system + 3 messages
    assert history[1]["content"] == "First"
    assert history[2]["content"] == "Second"
    assert history[3]["content"] == "Third"


@pytest.mark.asyncio
async def test_clear_history_removes_user_history(dialog_manager: DialogManager) -> None:
    """Тест: clear_history() удаляет историю пользователя"""
    user_id = 12345

    await dialog_manager.add_message(user_id, "user", "Hello")
    await dialog_manager.clear_history(user_id)

    # После очистки get_history создаёт новую историю
    history = await dialog_manager.get_history(user_id)
    assert len(history) == 1  # Только system prompt


@pytest.mark.asyncio
async def test_clear_history_does_not_affect_other_users(dialog_manager: DialogManager) -> None:
    """Тест: clear_history() не влияет на других пользователей"""
    user1_id = 111
    user2_id = 222

    await dialog_manager.add_message(user1_id, "user", "User 1 message")
    await dialog_manager.add_message(user2_id, "user", "User 2 message")

    await dialog_manager.clear_history(user1_id)

    history2 = await dialog_manager.get_history(user2_id)
    assert len(history2) == 2  # system + user message


def test_trim_history_with_max_context_zero_returns_full_history(
    config_with_max_context: Config, message_repository: MessageRepository
) -> None:
    """Тест: _trim_history() не обрезает при MAX_CONTEXT_MESSAGES = 0"""
    config_with_max_context.MAX_CONTEXT_MESSAGES = 0
    manager = DialogManager(config_with_max_context, message_repository)

    history: list[dict[str, Any]] = [
        {"role": "system", "content": "System"},
        {"role": "user", "content": "1"},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "3"},
        {"role": "assistant", "content": "4"},
    ]

    trimmed = manager._trim_history(history)

    assert len(trimmed) == 5  # Все сообщения сохранены


def test_trim_history_keeps_system_prompt_and_last_n_pairs(
    config_with_max_context: Config, message_repository: MessageRepository
) -> None:
    """Тест: _trim_history() обрезает контекст корректно при MAX_CONTEXT_MESSAGES > 0"""
    manager = DialogManager(config_with_max_context, message_repository)  # MAX_CONTEXT_MESSAGES = 2

    history: list[dict[str, Any]] = [
        {"role": "system", "content": "System"},
        {"role": "user", "content": "1"},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "3"},
        {"role": "assistant", "content": "4"},
        {"role": "user", "content": "5"},
        {"role": "assistant", "content": "6"},
    ]

    trimmed = manager._trim_history(history)

    # Должно остаться: system + последние 2*2 = 4 сообщения
    assert len(trimmed) == 5
    assert trimmed[0]["content"] == "System"
    assert trimmed[1]["content"] == "3"  # Последние 4 диалоговых сообщения
    assert trimmed[2]["content"] == "4"
    assert trimmed[3]["content"] == "5"
    assert trimmed[4]["content"] == "6"


def test_trim_history_handles_short_history(
    config_with_max_context: Config, message_repository: MessageRepository
) -> None:
    """Тест: _trim_history() корректно обрабатывает короткую историю"""
    manager = DialogManager(config_with_max_context, message_repository)

    history: list[dict[str, Any]] = [
        {"role": "system", "content": "System"},
        {"role": "user", "content": "1"},
    ]

    trimmed = manager._trim_history(history)

    assert len(trimmed) == 2  # Короткая история не обрезается


@pytest.mark.asyncio
async def test_get_history_applies_trimming_when_max_context_set(
    config_with_max_context: Config, message_repository: MessageRepository
) -> None:
    """Тест: get_history() применяет обрезку когда MAX_CONTEXT_MESSAGES > 0"""
    manager = DialogManager(config_with_max_context, message_repository)
    user_id = 12345

    # Добавляем много сообщений
    for i in range(10):
        await manager.add_message(user_id, "user", f"User {i}")
        await manager.add_message(user_id, "assistant", f"Assistant {i}")

    history = await manager.get_history(user_id)

    # Должно остаться: system + последние 2*2 = 4 сообщения
    assert len(history) == 5
    assert history[0]["role"] == "system"
    assert "User 8" in history[1]["content"]  # Последние пары
