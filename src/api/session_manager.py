"""Управление сессиями веб-пользователей"""

import hashlib
import uuid


def generate_session_id() -> str:
    """Генерация уникального session ID для веб-пользователя

    Returns:
        Session ID в формате "web_<uuid>"

    Example:
        >>> session_id = generate_session_id()
        >>> print(session_id)
        'web_550e8400-e29b-41d4-a716-446655440000'
    """
    return f"web_{uuid.uuid4()}"


def session_id_to_user_id(session_id: str) -> int:
    """Конвертация session ID в user_id для БД

    Использует SHA-256 хеширование и преобразование в положительное целое число
    в пределах 32-битного signed integer (чтобы не превысить лимиты SQLite).

    Args:
        session_id: Session ID веб-пользователя

    Returns:
        Целочисленный user_id для использования в БД

    Example:
        >>> user_id = session_id_to_user_id("web_550e8400-e29b-41d4-a716-446655440000")
        >>> print(user_id)
        1234567890
    """
    # Хешируем session_id
    hash_object = hashlib.sha256(session_id.encode())
    hash_hex = hash_object.hexdigest()

    # Берем первые 8 символов и конвертируем в int
    hash_int = int(hash_hex[:8], 16)

    # Убеждаемся, что значение положительное и в пределах 32-bit signed int
    # Максимальное значение: 2147483647 (2^31 - 1)
    user_id = hash_int % 2147483647

    # Гарантируем положительное значение
    return user_id if user_id > 0 else 1
