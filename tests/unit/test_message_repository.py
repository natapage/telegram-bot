"""Unit tests for MessageRepository class"""

import pytest

from src.message_repository import MessageRepository


@pytest.mark.asyncio
async def test_create_user(message_repository: MessageRepository) -> None:
    """Тест: create_user() создаёт пользователя"""
    user_id = 12345

    await message_repository.create_user(user_id)

    # Verify user was created by checking messages can be added
    await message_repository.add_message(user_id, "user", "Hello")
    messages = await message_repository.get_user_messages(user_id)
    assert len(messages) == 1


@pytest.mark.asyncio
async def test_create_user_idempotent(message_repository: MessageRepository) -> None:
    """Тест: create_user() идемпотентен (не создаёт дубликаты)"""
    user_id = 12345

    # Create user twice
    await message_repository.create_user(user_id)
    await message_repository.create_user(user_id)

    # Should not raise error and not create duplicate
    await message_repository.add_message(user_id, "user", "Hello")
    messages = await message_repository.get_user_messages(user_id)
    assert len(messages) == 1


@pytest.mark.asyncio
async def test_add_message(message_repository: MessageRepository) -> None:
    """Тест: add_message() добавляет сообщение с правильной длиной"""
    user_id = 12345
    content = "Test message"

    await message_repository.add_message(user_id, "user", content)

    messages = await message_repository.get_user_messages(user_id)
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == content
    assert messages[0]["length"] == len(content)
    assert messages[0]["is_deleted"] == 0


@pytest.mark.asyncio
async def test_add_multiple_messages(message_repository: MessageRepository) -> None:
    """Тест: add_message() добавляет несколько сообщений"""
    user_id = 12345

    await message_repository.add_message(user_id, "user", "First")
    await message_repository.add_message(user_id, "assistant", "Second")
    await message_repository.add_message(user_id, "user", "Third")

    messages = await message_repository.get_user_messages(user_id)
    assert len(messages) == 3
    assert messages[0]["content"] == "First"
    assert messages[1]["content"] == "Second"
    assert messages[2]["content"] == "Third"


@pytest.mark.asyncio
async def test_get_user_messages_ordered_by_created_at(message_repository: MessageRepository) -> None:
    """Тест: get_user_messages() возвращает сообщения в порядке created_at"""
    user_id = 12345

    await message_repository.add_message(user_id, "user", "First")
    await message_repository.add_message(user_id, "assistant", "Second")
    await message_repository.add_message(user_id, "user", "Third")

    messages = await message_repository.get_user_messages(user_id)

    # Check ordering
    assert messages[0]["content"] == "First"
    assert messages[1]["content"] == "Second"
    assert messages[2]["content"] == "Third"


@pytest.mark.asyncio
async def test_get_user_messages_filters_deleted(message_repository: MessageRepository) -> None:
    """Тест: get_user_messages() не возвращает удалённые сообщения"""
    user_id = 12345

    await message_repository.add_message(user_id, "user", "Message 1")
    await message_repository.add_message(user_id, "user", "Message 2")

    # Soft delete all messages
    await message_repository.soft_delete_user_messages(user_id)

    messages = await message_repository.get_user_messages(user_id)
    assert len(messages) == 0


@pytest.mark.asyncio
async def test_soft_delete_user_messages(message_repository: MessageRepository) -> None:
    """Тест: soft_delete_user_messages() помечает сообщения как удалённые"""
    user_id = 12345

    await message_repository.add_message(user_id, "user", "Message 1")
    await message_repository.add_message(user_id, "user", "Message 2")

    # Verify messages exist
    messages = await message_repository.get_user_messages(user_id)
    assert len(messages) == 2

    # Soft delete
    await message_repository.soft_delete_user_messages(user_id)

    # Verify messages are no longer returned
    messages = await message_repository.get_user_messages(user_id)
    assert len(messages) == 0


@pytest.mark.asyncio
async def test_soft_delete_does_not_affect_other_users(message_repository: MessageRepository) -> None:
    """Тест: soft_delete_user_messages() не влияет на других пользователей"""
    user1_id = 111
    user2_id = 222

    await message_repository.add_message(user1_id, "user", "User 1 message")
    await message_repository.add_message(user2_id, "user", "User 2 message")

    # Soft delete user 1 messages
    await message_repository.soft_delete_user_messages(user1_id)

    # User 2 messages should still exist
    user2_messages = await message_repository.get_user_messages(user2_id)
    assert len(user2_messages) == 1
    assert user2_messages[0]["content"] == "User 2 message"


@pytest.mark.asyncio
async def test_message_length_calculation(message_repository: MessageRepository) -> None:
    """Тест: add_message() правильно вычисляет длину сообщения"""
    user_id = 12345

    # Test with various length messages
    short_msg = "Hi"
    long_msg = "This is a much longer message with multiple words"

    await message_repository.add_message(user_id, "user", short_msg)
    await message_repository.add_message(user_id, "user", long_msg)

    messages = await message_repository.get_user_messages(user_id)

    assert messages[0]["length"] == len(short_msg)
    assert messages[1]["length"] == len(long_msg)

