# Правила разработки кода

> **Полная техническая спецификация**: См. [vision.md](./vision.md)

## Основные принципы

### 1. KISS (Keep It Simple, Stupid)
- Максимальная простота, никакого оверинжиниринга
- Без преждевременной абстракции и оптимизации
- Прямые, понятные решения

### 2. Один класс = Один файл
- Строгое правило: 1 класс на 1 файл
- Имя файла соответствует имени класса (snake_case для файла, PascalCase для класса)
- Чёткое разделение ответственности

### 3. Async/Await
- Все I/O операции используют `async`/`await`
- Вызовы Telegram API: async
- Вызовы LLM API: async

### 4. Type Hints
- Обязательны для всех параметров функций
- Обязательны для всех возвращаемых значений
- Использовать современный синтаксис Python 3.11+ (`list[str]` вместо `List[str]`)
- Пример: `def process_message(user_id: int, text: str) -> str:`
- Использовать `Protocol` для определения интерфейсов

### 5. Принципы качественного кода (SOLID)

**Single Responsibility Principle (SRP)**
- Один класс = одна ответственность (Config - только конфигурация, LLMClient - только работа с LLM)
- Если класс делает больше одного — разделить

**Open/Closed Principle**
- Открыт для расширения, закрыт для модификации
- Использовать Protocol для определения контрактов

**Dependency Injection**
- Передавай зависимости в `__init__()`, не создавай внутри класса
- Пример: `MessageHandler(llm_client, dialog_manager)` вместо создания внутри

**Fail Fast**
- Валидируй обязательные параметры в начале `__init__()`
- Валидируй входные данные перед обработкой (`if not message.text: return`)
- Выбрасывай исключение сразу, если что-то не так

**Explicit > Implicit**
- Избегай неявного поведения и скрытой магии
- Все зависимости и параметры должны быть видны явно

**DRY (Don't Repeat Yourself)**
- Не дублируй логику, выноси в отдельные функции/методы
- Переиспользуй код через композицию, а не копирование

## Структура проекта

```
src/
├── main.py              # Точка входа
├── bot.py               # Класс Bot
├── handler.py           # Класс MessageHandler
├── llm_client.py        # Класс LLMClient
├── dialog_manager.py    # Класс DialogManager
└── config.py            # Класс Config
```

## Логгирование

- Использовать библиотеку `structlog`
- Уровни: INFO для событий, ERROR для ошибок
- Формат: `logger.info("message_received", user_id=user_id, text=text)`
- JSON формат логов

## Обработка ошибок

- Простые блоки try/except для обработки специфичных ошибок
- Использовать кастомные исключения для бизнес-логики (`LLMAPIError`, `ConfigurationError`)
- Всегда обрабатывать `OpenAIError` и `asyncio.TimeoutError` для API вызовов
- Логировать ошибки с полным traceback: `logger.error("event", exc_info=True)`
- Понятные сообщения об ошибках для пользователя
- Не глушить исключения пустыми `except: pass`

## Конфигурация

- Загрузка из `.env` через `python-dotenv`
- Доступ через класс `Config`
- Никаких захардкоженных значений
- Валидация обязательных параметров в `__init__()`

---

## Форматирование и стиль кода

### Инструменты
- **Форматтер**: `ruff format` (автоматическое форматирование)
- **Линтер**: `ruff check` (проверка стиля и потенциальных ошибок)
- **Type Checker**: `mypy` (проверка типов)

### Параметры форматирования
- Длина строки: 120 символов
- Отступы: 4 пробела (никаких табов)
- Сортировка импортов: автоматическая через ruff (stdlib → third-party → first-party)
- Пустые строки: 2 между классами/функциями верхнего уровня, 1 между методами

### Правила именования
- **Классы**: `PascalCase` (Config, DialogManager)
- **Функции/методы**: `snake_case` (get_history, add_message)
- **Константы**: `UPPER_SNAKE_CASE` (MAX_CONTEXT_MESSAGES)
- **Приватные методы**: `_snake_case` (_trim_history)
- **Переменные**: `snake_case` (user_id, message_text)

### Docstrings
- Использовать Google Style для всех публичных классов, методов, функций
- Формат:
```python
def method(param: str) -> int:
    """Краткое описание метода

    Args:
        param: Описание параметра

    Returns:
        Описание возвращаемого значения

    Raises:
        ValueError: Описание ошибки
    """
```

---

## Контроль качества кода

### Обязательные проверки перед коммитом
```bash
make format  # Автоформатирование
make lint    # Ruff + Mypy проверки
make test    # Запуск тестов (если есть)
```

### Настройка ruff
- Правила: E (errors), F (pyflakes), I (isort), N (naming), UP (pyupgrade), B (bugbear), C4, SIM (simplify), TCH (type checking)
- Игнорировать: E501 (длина строки, т.к. установлено 120)
- Target: Python 3.11+

### Настройка mypy
- Режим: `strict = true`
- Требование: `disallow_untyped_defs = true`
- Все функции должны иметь type hints

### Метрики качества
- **Линтер**: 0 ошибок перед коммитом
- **Type coverage**: 100% (все функции типизированы)
- **Test coverage**: >= 80% для критичных компонентов

---

## Тестирование

### Стратегия тестирования
- **Unit-тесты**: для бизнес-логики (DialogManager, Config)
- **Integration-тесты**: для взаимодействия компонентов (MessageHandler)
- **Mock-тесты**: для внешних API (LLMClient с AsyncOpenAI)

### Инструменты
- **Framework**: pytest
- **Async поддержка**: pytest-asyncio
- **Coverage**: pytest-cov
- **Mocking**: unittest.mock (AsyncMock для async функций)

### Структура тестов
```
tests/
├── __init__.py
├── conftest.py          # Общие fixtures
├── unit/                # Unit-тесты
│   ├── test_config.py
│   ├── test_dialog_manager.py
│   └── test_llm_client.py
└── integration/         # Integration-тесты
    └── test_handler.py
```

### Правила написания тестов
- Один тест проверяет одну вещь
- Использовать fixtures для переиспользования setup кода
- Использовать `monkeypatch` для мока переменных окружения
- Использовать `AsyncMock` для мока async функций
- Тесты должны быть независимыми и воспроизводимыми
- Имена тестов: `test_<что_тестируем>_<ожидаемый_результат>`

### Пример теста
```python
@pytest.mark.asyncio
async def test_generate_response_returns_content(llm_client, mock_openai):
    """Тест: generate_response возвращает корректный ответ от API"""
    mock_openai.chat.completions.create.return_value = MockResponse("Hello")

    result = await llm_client.generate_response([{"role": "user", "content": "Hi"}])

    assert result == "Hello"
```

---

## Лучшие практики Python

### Работа с async/await
- Не блокировать event loop синхронными операциями
- Использовать `asyncio.gather()` для параллельных операций
- Правильно обрабатывать `asyncio.TimeoutError` и `asyncio.CancelledError`

### Работа с типами
- Предпочитать встроенные generic types: `list[str]` вместо `List[str]`
- Использовать `typing.Protocol` для duck typing
- Использовать `Optional[T]` только когда значение действительно может быть None
- Не использовать `Any` без крайней необходимости

### Работа со строками
- Использовать f-strings: `f"User {user_id}"` вместо `"User " + str(user_id)`
- Избегать конкатенации в циклах, использовать `"".join()`

### Работа с коллекциями
- Использовать comprehensions: `[x for x in items if x > 0]`
- Использовать `dict.get()` для безопасного доступа к ключам
- Предпочитать `dict[key]` для обязательных ключей (Fail Fast)

### Работа с ресурсами
- Использовать context managers (`async with`) для cleanup
- Не забывать закрывать соединения и файлы
- Использовать `pathlib.Path` вместо `os.path`

### Обработка None
- Проверять на None явно: `if value is None:` вместо `if not value:`
- Использовать early return для упрощения логики:
```python
if not message.text:
    return
# основная логика
```

---

**Справка**: Полная архитектура, модели данных и сценарии в [vision.md](./vision.md)
