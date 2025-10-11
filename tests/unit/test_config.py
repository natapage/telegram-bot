"""Unit tests for Config class"""

from unittest.mock import patch

import pytest

from src.config import Config


def test_config_loads_required_parameters(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: успешная загрузка всех обязательных параметров"""
    with patch("src.config.load_dotenv"):  # Мокируем load_dotenv
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")

        config = Config()

        assert config.TELEGRAM_BOT_TOKEN == "test_bot_token"
        assert config.OPENAI_API_KEY == "test_api_key"
        assert config.SYSTEM_PROMPT == "Test prompt"


def test_config_raises_error_when_telegram_bot_token_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: выброс ValueError при отсутствии TELEGRAM_BOT_TOKEN"""
    with patch("src.config.load_dotenv"):
        monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")

        with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
            Config()


def test_config_raises_error_when_openai_api_key_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: выброс ValueError при отсутствии OPENAI_API_KEY"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")

        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            Config()


def test_config_raises_error_when_system_prompt_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: выброс ValueError при отсутствии SYSTEM_PROMPT"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.delenv("SYSTEM_PROMPT", raising=False)

        with pytest.raises(ValueError, match="SYSTEM_PROMPT"):
            Config()


def test_config_uses_default_values_for_optional_parameters(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: корректные дефолтные значения для необязательных параметров"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")
        # Удаляем опциональные переменные
        monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
        monkeypatch.delenv("OPENAI_MODEL", raising=False)
        monkeypatch.delenv("LOG_LEVEL", raising=False)
        monkeypatch.delenv("LOG_FILE_PATH", raising=False)
        monkeypatch.delenv("MAX_CONTEXT_MESSAGES", raising=False)

        config = Config()

        assert config.OPENAI_BASE_URL == "https://openrouter.ai/api/v1"
        assert config.OPENAI_MODEL == "openai/gpt-4"
        assert config.LOG_LEVEL == "INFO"
        assert config.LOG_FILE_PATH == "logs/"
        assert config.MAX_CONTEXT_MESSAGES == 0


def test_config_overrides_default_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: переопределение дефолтных значений через переменные окружения"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")
        monkeypatch.setenv("OPENAI_BASE_URL", "https://custom.api/v1")
        monkeypatch.setenv("OPENAI_MODEL", "custom/model")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("LOG_FILE_PATH", "custom_logs/")
        monkeypatch.setenv("MAX_CONTEXT_MESSAGES", "5")

        config = Config()

        assert config.OPENAI_BASE_URL == "https://custom.api/v1"
        assert config.OPENAI_MODEL == "custom/model"
        assert config.LOG_LEVEL == "DEBUG"
        assert config.LOG_FILE_PATH == "custom_logs/"
        assert config.MAX_CONTEXT_MESSAGES == 5


def test_config_converts_max_context_messages_to_int(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: конвертация MAX_CONTEXT_MESSAGES в int"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")
        monkeypatch.setenv("MAX_CONTEXT_MESSAGES", "10")

        config = Config()

        assert isinstance(config.MAX_CONTEXT_MESSAGES, int)
        assert config.MAX_CONTEXT_MESSAGES == 10


def test_config_loads_bot_role_name_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: загрузка BOT_ROLE_NAME из переменной окружения"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")
        monkeypatch.setenv("BOT_ROLE_NAME", "Консультант по выбору музыки")

        config = Config()

        assert config.BOT_ROLE_NAME == "Консультант по выбору музыки"


def test_config_loads_bot_role_description_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: загрузка BOT_ROLE_DESCRIPTION из переменной окружения"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")
        monkeypatch.setenv("BOT_ROLE_DESCRIPTION", "Помогаю найти музыку по настроению")

        config = Config()

        assert config.BOT_ROLE_DESCRIPTION == "Помогаю найти музыку по настроению"


def test_config_has_default_bot_role_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: дефолтные значения для BOT_ROLE_NAME и BOT_ROLE_DESCRIPTION"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")
        # Не устанавливаем BOT_ROLE_* переменные
        monkeypatch.delenv("BOT_ROLE_NAME", raising=False)
        monkeypatch.delenv("BOT_ROLE_DESCRIPTION", raising=False)

        config = Config()

        assert config.BOT_ROLE_NAME == "ИИ-ассистент"
        assert config.BOT_ROLE_DESCRIPTION == "Помогаю отвечать на вопросы"


def test_config_loads_system_prompt_from_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pytest.TempPathFactory
) -> None:
    """Тест: загрузка системного промпта из файла"""
    # Создаем временный файл с промптом
    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text("Test prompt from file", encoding="utf-8")

    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT_FILE", str(prompt_file))
        monkeypatch.delenv("SYSTEM_PROMPT", raising=False)

        config = Config()

        assert config.SYSTEM_PROMPT == "Test prompt from file"


def test_config_falls_back_to_env_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: fallback на SYSTEM_PROMPT из env если файл не указан"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt from env")
        monkeypatch.delenv("SYSTEM_PROMPT_FILE", raising=False)

        config = Config()

        assert config.SYSTEM_PROMPT == "Test prompt from env"


def test_config_raises_error_when_no_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: выброс ValueError когда нет ни файла, ни переменной окружения"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.delenv("SYSTEM_PROMPT", raising=False)
        monkeypatch.delenv("SYSTEM_PROMPT_FILE", raising=False)

        with pytest.raises(ValueError, match="Системный промпт не настроен"):
            Config()


def test_config_raises_error_when_prompt_file_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: выброс ValueError когда файл промпта не существует"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
        monkeypatch.setenv("SYSTEM_PROMPT_FILE", "non_existent_file.txt")
        monkeypatch.delenv("SYSTEM_PROMPT", raising=False)

        with pytest.raises(ValueError, match="Файл системного промпта не найден"):
            Config()
