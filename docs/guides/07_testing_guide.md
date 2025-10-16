# Testing Guide

Как писать и запускать тесты.

## Структура тестов

```
tests/
├── __init__.py
├── conftest.py          # Общие fixtures
├── unit/                # Unit-тесты (изолированные)
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_dialog_manager.py
│   └── test_llm_client.py
└── integration/         # Integration-тесты
    ├── __init__.py
    └── test_handler.py
```

## Запуск тестов

### Все тесты

```bash
make test
```

Выполняет: `uv run pytest tests/ -v`

### С coverage

```bash
make test-cov
```

Выполняет: `uv run pytest tests/ -v --cov=src --cov-report=term-missing`

**Текущий минимум**: 60% coverage

### Конкретный файл

```bash
uv run pytest tests/unit/test_config.py -v
```

### Конкретный тест

```bash
uv run pytest tests/unit/test_config.py::test_config_loads_required_params -v
```

## Fixtures (conftest.py)

### config

Мокированная конфигурация с базовыми параметрами:

```python
@pytest.fixture
def config(monkeypatch: pytest.MonkeyPatch) -> Config:
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token_123")
        monkeypatch.setenv("OPENAI_API_KEY", "test_api_key_123")
        monkeypatch.setenv("SYSTEM_PROMPT", "You are a test assistant")
        return Config()
```

**Использование**:
```python
def test_something(config):
    assert config.TELEGRAM_BOT_TOKEN == "test_bot_token_123"
```

### config_with_max_context

Конфигурация с ограничением контекста:

```python
@pytest.fixture
def config_with_max_context(monkeypatch: pytest.MonkeyPatch) -> Config:
    with patch("src.config.load_dotenv"):
        # ... базовые параметры
        monkeypatch.setenv("MAX_CONTEXT_MESSAGES", "2")
        return Config()
```

**Использование**:
```python
def test_trim_history(config_with_max_context):
    dm = DialogManager(config_with_max_context)
    # тестирование обрезки
```

### dialog_manager

DialogManager с тестовой конфигурацией:

```python
@pytest.fixture
def dialog_manager(config: Config) -> DialogManager:
    return DialogManager(config)
```

### logger

Мокированный structlog logger:

```python
@pytest.fixture
def logger() -> MagicMock:
    mock_logger = MagicMock()
    mock_logger.info = MagicMock()
    mock_logger.error = MagicMock()
    return mock_logger
```

## Unit-тесты примеры

### test_config.py

**Тестирование загрузки параметров**:

```python
def test_config_loads_required_params(config):
    """Тест: Config загружает обязательные параметры"""
    assert config.TELEGRAM_BOT_TOKEN == "test_bot_token_123"
    assert config.OPENAI_API_KEY == "test_api_key_123"
    assert config.SYSTEM_PROMPT == "You are a test assistant"
```

**Тестирование валидации**:

```python
def test_config_raises_error_when_token_missing(monkeypatch):
    """Тест: Config выбрасывает ValueError если токен отсутствует"""
    with patch("src.config.load_dotenv"):
        monkeypatch.setenv("OPENAI_API_KEY", "test")
        monkeypatch.setenv("SYSTEM_PROMPT", "test")
        # TELEGRAM_BOT_TOKEN отсутствует

        with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
            Config()
```

**Тестирование дефолтов**:

```python
def test_config_has_default_values(config):
    """Тест: Config имеет корректные дефолтные значения"""
    assert config.OPENAI_BASE_URL == "https://openrouter.ai/api/v1"
    assert config.OPENAI_MODEL == "openai/gpt-4"
    assert config.LOG_LEVEL == "INFO"
    assert config.MAX_CONTEXT_MESSAGES == 0
```

### test_dialog_manager.py

**Тестирование создания истории**:

```python
def test_get_history_creates_new_history_with_system_prompt(dialog_manager, config):
    """Тест: get_history() создаёт новую историю с системным промптом"""
    user_id = 12345

    history = dialog_manager.get_history(user_id)

    assert len(history) == 1
    assert history[0]["role"] == "system"
    assert history[0]["content"] == config.SYSTEM_PROMPT
```

**Тестирование добавления сообщений**:

```python
def test_add_message_appends_to_history(dialog_manager):
    """Тест: add_message() добавляет сообщение в историю"""
    user_id = 12345

    dialog_manager.add_message(user_id, "user", "Hello")
    history = dialog_manager.get_history(user_id)

    assert len(history) == 2  # system + user
    assert history[1]["role"] == "user"
    assert history[1]["content"] == "Hello"
```

**Тестирование очистки**:

```python
def test_clear_history_removes_user_history(dialog_manager):
    """Тест: clear_history() удаляет историю пользователя"""
    user_id = 12345

    dialog_manager.add_message(user_id, "user", "Hello")
    dialog_manager.clear_history(user_id)

    assert user_id not in dialog_manager.dialogs
```

**Тестирование обрезки контекста**:

```python
def test_trim_history_limits_context(config_with_max_context):
    """Тест: _trim_history() обрезает историю до MAX_CONTEXT_MESSAGES"""
    dm = DialogManager(config_with_max_context)
    user_id = 12345

    # Добавить 6 пар сообщений (12 сообщений + system = 13)
    for i in range(6):
        dm.add_message(user_id, "user", f"msg{i}")
        dm.add_message(user_id, "assistant", f"resp{i}")

    history = dm.get_history(user_id)

    # MAX_CONTEXT_MESSAGES=2 → system + 4 последних сообщения
    assert len(history) == 5
    assert history[0]["role"] == "system"
    assert history[1]["content"] == "msg4"  # предпоследняя пара
    assert history[-1]["content"] == "resp5"  # последняя пара
```

### test_llm_client.py

**Мокирование AsyncOpenAI**:

```python
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_openai():
    """Мок для AsyncOpenAI"""
    with patch("src.llm_client.AsyncOpenAI") as mock:
        instance = mock.return_value
        instance.chat.completions.create = AsyncMock()
        yield instance
```

**Тестирование успешного ответа**:

```python
@pytest.mark.asyncio
async def test_generate_response_returns_content(config, logger, mock_openai):
    """Тест: generate_response() возвращает корректный ответ"""
    # Настроить мок
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello from LLM"
    mock_openai.chat.completions.create.return_value = mock_response

    # Создать клиент и вызвать
    client = LLMClient(config, logger)
    result = await client.generate_response([{"role": "user", "content": "Hi"}])

    # Проверить
    assert result == "Hello from LLM"
    assert mock_openai.chat.completions.create.called
```

**Тестирование обработки ошибок**:

```python
from openai import OpenAIError

@pytest.mark.asyncio
async def test_generate_response_handles_api_error(config, logger, mock_openai):
    """Тест: generate_response() обрабатывает OpenAIError"""
    # Настроить мок для выброса ошибки
    mock_openai.chat.completions.create.side_effect = OpenAIError("API Error")

    # Создать клиент
    client = LLMClient(config, logger)

    # Проверить что ошибка пробрасывается
    with pytest.raises(OpenAIError):
        await client.generate_response([{"role": "user", "content": "Hi"}])

    # Проверить что ошибка залогирована
    logger.error.assert_called_once()
```

**Тестирование логирования**:

```python
@pytest.mark.asyncio
async def test_generate_response_logs_request_and_response(config, logger, mock_openai):
    """Тест: generate_response() логирует запрос и ответ"""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Response"
    mock_openai.chat.completions.create.return_value = mock_response

    client = LLMClient(config, logger)
    await client.generate_response([{"role": "user", "content": "Hi"}])

    # Проверить логи
    assert logger.info.call_count == 2  # request + response
    logger.info.assert_any_call("llm_request", model="openai/gpt-4", message_count=1)
    logger.info.assert_any_call("llm_response", length=8)
```

## Integration-тесты

### test_handler.py

**Мокирование зависимостей**:

```python
@pytest.fixture
def handler(config, logger):
    """MessageHandler с мокированными зависимостями"""
    mock_llm = AsyncMock()
    mock_llm.generate_response.return_value = "LLM response"

    dialog_manager = DialogManager(config)

    return MessageHandler(mock_llm, dialog_manager, logger)
```

**Тестирование команд**:

```python
@pytest.mark.asyncio
async def test_handle_start_sends_greeting(handler):
    """Тест: handle_start отправляет приветствие"""
    mock_message = AsyncMock()

    await handler.handle_start(mock_message)

    mock_message.answer.assert_called_once_with("Привет! Я LLM-ассистент")
```

## Мокирование

### monkeypatch (для env)

```python
def test_with_custom_env(monkeypatch):
    monkeypatch.setenv("MY_VAR", "test_value")
    # теперь os.getenv("MY_VAR") вернет "test_value"
```

### patch (для модулей)

```python
from unittest.mock import patch

def test_with_patched_module():
    with patch("src.config.load_dotenv"):
        # load_dotenv не будет вызван
        config = Config()
```

### AsyncMock (для async функций)

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_function():
    mock_func = AsyncMock(return_value="result")
    result = await mock_func()
    assert result == "result"
```

### MagicMock (для sync функций)

```python
from unittest.mock import MagicMock

def test_sync_function():
    mock_obj = MagicMock()
    mock_obj.method.return_value = "result"
    assert mock_obj.method() == "result"
```

## Best Practices

### Именование тестов

```python
# ✅ Правильно
def test_get_history_creates_new_history_with_system_prompt():
    """Тест: get_history() создаёт новую историю с системным промптом"""
    ...

# ❌ Неправильно
def test_1():
    ...
```

**Формат**: `test_<что_тестируем>_<ожидаемый_результат>`

### Docstrings в тестах

```python
def test_something():
    """Тест: краткое описание что проверяется"""
    ...
```

### Один тест - одна вещь

```python
# ✅ Правильно
def test_add_message_appends_to_history():
    # проверяем только добавление

def test_add_message_increments_length():
    # проверяем только длину

# ❌ Неправильно
def test_add_message():
    # проверяем и добавление, и длину, и содержимое, и ...
```

### Fixtures переиспользование

```python
# ✅ Правильно - fixture в conftest.py
@pytest.fixture
def dialog_manager(config):
    return DialogManager(config)

# Использовать в тестах
def test_something(dialog_manager):
    ...

# ❌ Неправильно - создавать в каждом тесте
def test_something(config):
    dm = DialogManager(config)
    ...
```

## Coverage

### Проверка coverage

```bash
make test-cov
```

**Вывод**:
```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/config.py                40      5    87%   45-49
src/dialog_manager.py        35      2    94%   67-68
src/llm_client.py            28      3    89%   52-54
-------------------------------------------------------
TOTAL                       103     10    90%
```

### Текущая конфигурация

```toml
# pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "src/main.py",      # точка входа
    "src/bot.py",       # простая обертка aiogram
]

[tool.coverage.report]
fail_under = 60
```

**Минимум**: 60%
**Цель**: 80% для критичных компонентов

## Добавление нового теста

### Шаги

**1. Определить что тестировать**:
- Новый метод
- Edge case
- Error handling

**2. Выбрать тип теста**:
- Unit (изолированный компонент)
- Integration (взаимодействие)

**3. Создать тест**:
```python
# tests/unit/test_my_component.py
def test_my_new_feature(config):
    """Тест: описание"""
    component = MyComponent(config)
    result = component.new_method()
    assert result == expected
```

**4. Запустить**:
```bash
uv run pytest tests/unit/test_my_component.py::test_my_new_feature -v
```

**5. Проверить coverage**:
```bash
make test-cov
```

## Следующие шаги

- Прочитать [Code Review Guide](08_code_review_guide.md) для ревью тестов
- Изучить [Development Workflow](06_development_workflow.md) для TDD процесса
- Посмотреть [Troubleshooting](10_troubleshooting.md) если тесты падают
