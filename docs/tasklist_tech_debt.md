# План технического долга и улучшений качества кода

## 📊 Прогресс

| Итерация | Задача | Статус | Дата |
|----------|--------|--------|------|
| 1 | Критичные исправления кода | 🟢 Завершено | 2025-10-11 |
| 2 | Инструменты контроля качества | 🟢 Завершено | 2025-10-11 |
| 3 | Базовое тестирование | 🔵 Не начато | - |
| 4 | Архитектурный рефакторинг | 🔵 Не начато | - |

**Легенда**: 🔵 Не начато | 🟡 В процессе | 🟢 Завершено

---

## Итерация 1: Критичные исправления кода

**Цель**: Устранить критичные баги и улучшить обработку ошибок

### Валидация входных данных
- [x] Добавить проверку `if not message.text: return` в `handle_text()` (handler.py:64)
- [x] Добавить валидацию `message.from_user` на None перед получением `user_id`

### Обработка ошибок LLM API
- [x] Обернуть `client.chat.completions.create()` в try/except (llm_client.py:36)
- [x] Импортировать `OpenAIError` из библиотеки `openai`
- [x] Обработать `asyncio.TimeoutError` отдельно
- [x] Логировать ошибки API с `self.logger.error("llm_api_error", error=str(e))`
- [x] Re-raise исключение для обработки в handler

### Применение MAX_CONTEXT_MESSAGES
- [x] Создать метод `_trim_history(history: list[dict]) -> list[dict]` в DialogManager
- [x] Реализовать обрезку: системный промпт + последние N*2 сообщений (user+assistant пары)
- [x] Вызывать `_trim_history()` в методе `get_history()`
- [x] Добавить логирование при обрезке контекста

### Проверка соответствия соглашениям
- [x] Проверить все type hints на соответствие conventions.md
- [x] Проверить docstrings во всех методах
- [x] Проверить соответствие архитектуре из vision.md
- [x] Проверить использование async/await для всех I/O операций

**Тест**: Запустить бота, отправить пустое сообщение (не должно крашиться), отключить интернет (должна быть корректная ошибка), проверить обрезку контекста при MAX_CONTEXT_MESSAGES=5

---

## Итерация 2: Инструменты контроля качества

**Цель**: Настроить автоматизированные инструменты для проверки качества кода

### Конфигурация ruff (форматтер + линтер)
- [x] Добавить зависимость: `uv add --dev ruff`
- [x] Создать секцию `[tool.ruff]` в pyproject.toml
- [x] Установить `line-length = 120`
- [x] Установить `target-version = "py311"`
- [x] Включить правила: `select = ["E", "F", "I", "N", "UP", "B", "C4", "SIM", "TCH"]`
- [x] Настроить `[tool.ruff.lint.isort]` с `known-first-party = ["src"]`

### Конфигурация mypy (type checker)
- [x] Добавить зависимость: `uv add --dev mypy`
- [x] Создать секцию `[tool.mypy]` в pyproject.toml
- [x] Установить `python_version = "3.11"`
- [x] Установить `strict = true`
- [x] Установить `disallow_untyped_defs = true`

### Makefile команды
- [x] Добавить команду `make format` для `ruff format src/`
- [x] Добавить команду `make lint` для `ruff check src/ && mypy src/`
- [x] Добавить команду `make fix` для `ruff check src/ --fix`
- [x] Обновить существующий Makefile, не удаляя команду `run`

### Первый прогон и исправления
- [x] Запустить `make format` и закоммитить изменения
- [x] Запустить `make lint` и исправить все ошибки ruff
- [x] Исправить все ошибки mypy (добавить недостающие type hints)

### Проверка соответствия соглашениям
- [x] Проверить, что все файлы следуют правилу "1 класс = 1 файл"
- [x] Проверить соответствие именования файлов (snake_case)
- [x] Проверить соответствие vision.md: структура проекта
- [x] Проверить следование принципам KISS из conventions.md

**Тест**: Выполнить `make lint` без ошибок, выполнить `make format` и убедиться что код не изменился (уже отформатирован)

---

## Итерация 3: Базовое тестирование

**Цель**: Покрыть тестами критичные компоненты

### Настройка pytest
- [ ] Добавить зависимости: `uv add --dev pytest pytest-asyncio pytest-cov`
- [ ] Создать директорию `tests/` с подпапками `unit/` и `integration/`
- [ ] Создать файл `tests/__init__.py` (пустой)
- [ ] Создать `tests/conftest.py` с базовыми fixtures

### Fixtures и моки
- [ ] Создать fixture `config` с моком переменных окружения через `monkeypatch`
- [ ] Создать fixture `dialog_manager` с использованием `config`
- [ ] Создать fixture `logger` с моком structlog.BoundLogger

### Unit-тесты для Config
- [ ] Создать `tests/unit/test_config.py`
- [ ] Тест: успешная загрузка всех обязательных параметров
- [ ] Тест: выброс ValueError при отсутствии TELEGRAM_BOT_TOKEN
- [ ] Тест: выброс ValueError при отсутствии OPENAI_API_KEY
- [ ] Тест: выброс ValueError при отсутствии SYSTEM_PROMPT
- [ ] Тест: корректные дефолтные значения для необязательных параметров

### Unit-тесты для DialogManager
- [ ] Создать `tests/unit/test_dialog_manager.py`
- [ ] Тест: `get_history()` создаёт новую историю с системным промптом
- [ ] Тест: `add_message()` добавляет сообщение в историю
- [ ] Тест: `clear_history()` удаляет историю пользователя
- [ ] Тест: `_trim_history()` обрезает контекст корректно при MAX_CONTEXT_MESSAGES > 0
- [ ] Тест: `_trim_history()` не обрезает при MAX_CONTEXT_MESSAGES = 0

### Unit-тесты для LLMClient
- [ ] Создать `tests/unit/test_llm_client.py`
- [ ] Использовать `unittest.mock.AsyncMock` для мока AsyncOpenAI
- [ ] Тест: успешный вызов `generate_response()` возвращает корректный ответ
- [ ] Тест: обработка OpenAIError при ошибке API
- [ ] Тест: логирование запроса и ответа

### Makefile и coverage
- [ ] Добавить команду `make test` для `pytest tests/ -v`
- [ ] Добавить команду `make test-cov` для `pytest tests/ -v --cov=src --cov-report=term-missing`
- [ ] Добавить секцию `[tool.coverage.run]` в pyproject.toml с `source = ["src"]`
- [ ] Установить `[tool.coverage.report]` с `fail_under = 80`

### Проверка соответствия соглашениям
- [ ] Проверить, что тесты используют type hints
- [ ] Проверить, что async тесты используют `@pytest.mark.asyncio`
- [ ] Проверить соответствие vision.md: принцип "без тестов на начальном этапе" заменён на "базовое покрытие"
- [ ] Проверить следование Dependency Injection в тестах

**Тест**: Запустить `make test` - все тесты должны пройти, запустить `make test-cov` - coverage >= 80%

---

## Итерация 4: Архитектурный рефакторинг

**Цель**: Улучшить архитектуру кода с применением SOLID принципов

### Создание Protocol интерфейсов
- [ ] Создать файл `src/protocols.py`
- [ ] Определить `LLMClientProtocol(Protocol)` с методом `generate_response()`
- [ ] Определить `DialogManagerProtocol(Protocol)` с методами `get_history()`, `add_message()`, `clear_history()`
- [ ] Обновить type hints в MessageHandler для использования Protocol

### Разделение DialogManager (SRP)
- [ ] Создать файл `src/dialog_repository.py` с классом `DialogRepository`
- [ ] Переместить хранение `dialogs: dict[int, list[dict]]` в DialogRepository
- [ ] Создать файл `src/dialog_context_service.py` с классом `DialogContextService`
- [ ] Переместить логику обрезки контекста в DialogContextService
- [ ] Обновить DialogManager как фасад над Repository и Service
- [ ] Обновить тесты для новых классов

### Dependency Injection контейнер
- [ ] Рефакторить `main.py` для явного создания зависимостей
- [ ] Группировать создание зависимостей в функцию `setup_dependencies(config, logger)`
- [ ] Возвращать tuple или dataclass с компонентами

### Улучшение error handling
- [ ] Создать файл `src/exceptions.py` с кастомными исключениями
- [ ] Определить `LLMAPIError(Exception)` для ошибок LLM API
- [ ] Определить `ConfigurationError(Exception)` для ошибок конфигурации
- [ ] Заменить ValueError в Config на ConfigurationError
- [ ] Обернуть OpenAIError в LLMAPIError в LLMClient

### Проверка соответствия соглашениям
- [ ] Проверить Single Responsibility для всех классов
- [ ] Проверить Dependency Injection во всех конструкторах
- [ ] Проверить соответствие vision.md: "1 класс = 1 файл"
- [ ] Проверить отсутствие нарушений KISS (избыточной абстракции)

### Финальная проверка
- [ ] Запустить `make lint` без ошибок
- [ ] Запустить `make test-cov` с coverage >= 80%
- [ ] Запустить `make run` и протестировать бота вручную
- [ ] Обновить README.md с новыми командами Makefile
- [ ] Проверить все docstrings на актуальность после рефакторинга

**Тест**: Полный цикл - `make format && make lint && make test-cov && make run`, бот работает без изменения функциональности, код чище и поддерживаемее

---

**Справка**:
- Соглашения: [conventions.md](./conventions.md)
- Архитектура: [vision.md](./vision.md)
- Основной plan: [tasklist.md](./tasklist.md)
