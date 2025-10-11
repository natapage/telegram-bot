# Техническое видение проекта: LLM-ассистент Telegram-бот

## 1. Технологии

### Базовые технологии
- **Python 3.11+** - язык разработки
- **uv** - управление зависимостями и виртуальным окружением
- **make** - автоматизация задач (запуск, форматирование)

### Telegram интеграция
- **aiogram 3.x** - асинхронная библиотека для Telegram Bot API
- **polling** - метод получения обновлений от Telegram

### Работа с LLM
- **openai** - клиент для взаимодействия с OpenAI-совместимым API
- **Openrouter** - провайдер для доступа к различным LLM моделям

### Вспомогательные библиотеки
- **python-dotenv** - управление переменными окружения через .env файлы
- **structlog** - структурированное логирование

### Инструменты качества кода
- **ruff** - форматтер и линтер (замена black, flake8, isort)
- **mypy** - статический анализатор типов
- **pytest** - фреймворк для тестирования
- **pytest-asyncio** - поддержка async тестов
- **pytest-cov** - покрытие кода тестами

### Хранение данных
- **In-memory** - история диалогов хранится в памяти (словарь Python)
- База данных не используется на начальном этапе

## 2. Принцип разработки

### Архитектурные принципы
- **KISS (Keep It Simple, Stupid)** - максимальная простота, без избыточной абстракции
- **ООП** - 1 класс = 1 файл, чёткое разделение ответственности
- **Асинхронность** - async/await для всех I/O операций (Telegram, LLM API)

### Принципы кода
- **Single Responsibility** - каждый класс отвечает за одну задачу
- **Dependency Injection** - простая инъекция зависимостей через конструктор
- **Fail Fast** - быстрое обнаружение ошибок при инициализации
- **Explicit is better than implicit** - явность лучше неявности
- Минимум магии и метапрограммирования
- Простые понятные названия классов, методов и переменных

### Подход к разработке
- Итеративно: сначала минимальный рабочий прототип, затем улучшения
- Без преждевременной оптимизации
- Контроль качества кода: форматтеры, линтеры, type checkers
- Базовое покрытие тестами критичных компонентов (>= 80%)
- Рефакторинг по принципам SOLID при необходимости

## 3. Структура проекта

```
telegram-bot/
├── src/
│   ├── __init__.py
│   ├── main.py              # Точка входа приложения
│   ├── bot.py               # Класс Bot - инициализация aiogram
│   ├── handler.py           # Класс MessageHandler - обработка сообщений
│   ├── llm_client.py        # Класс LLMClient - работа с LLM
│   ├── dialog_manager.py    # Класс DialogManager - управление историей
│   ├── config.py            # Класс Config - конфигурация
│   ├── protocols.py         # Protocol интерфейсы (опционально)
│   └── exceptions.py        # Кастомные исключения (опционально)
├── tests/                   # Тесты (добавляются по мере развития)
│   ├── __init__.py
│   ├── conftest.py          # Общие fixtures
│   ├── unit/                # Unit-тесты
│   │   ├── test_config.py
│   │   ├── test_dialog_manager.py
│   │   └── test_llm_client.py
│   └── integration/         # Integration-тесты
│       └── test_handler.py
├── docs/
│   ├── idea.md              # Идея проекта
│   ├── vision.md            # Техническое видение
│   ├── conventions.md       # Правила разработки кода
│   ├── tasklist.md          # План разработки
│   ├── tasklist_tech_debt.md # План технического долга
│   ├── workflow.md          # Процесс выполнения работ
│   └── workflow_tech_debt.md # Процесс с контролем качества
├── logs/                    # Логи приложения (в .gitignore)
├── .env.example             # Пример переменных окружения
├── .env                     # Реальные переменные (в .gitignore)
├── .gitignore
├── Makefile                 # Команды для запуска и управления
├── pyproject.toml           # Конфигурация проекта для uv
└── README.md
```

### Принципы организации
- **1 класс = 1 файл** в директории `src/`
- Все исходники в директории `src/`
- Все тесты в директории `tests/`
- Документация в директории `docs/`
- Конфигурация через `.env` файл
- Настройки инструментов в `pyproject.toml`

## 4. Архитектура проекта

### Схема компонентов

```
main.py
   ↓
Bot (aiogram Dispatcher + Router)
   ↓
MessageHandler
   ↓ ↓
   ↓ DialogManager (хранит историю)
   ↓
LLMClient (общается с Openrouter)
   ↑
Config (настройки из .env)
```

### Компоненты и их роли

1. **main.py** - создаёт Config, создаёт Bot, запускает polling
2. **Bot** - инициализирует aiogram, регистрирует MessageHandler, запускает polling
3. **MessageHandler** - получает сообщения от пользователей, валидирует входные данные, взаимодействует с DialogManager и LLMClient, отправляет ответы
4. **DialogManager** - хранит историю диалогов в словаре `{user_id: [messages]}`, применяет обрезку контекста
5. **LLMClient** - формирует запрос к LLM, отправляет через openai client к Openrouter, обрабатывает ошибки API, возвращает ответ
6. **Config** - загружает переменные из .env, валидирует обязательные параметры

**Опциональные компоненты (при рефакторинге):**
- **protocols.py** - Protocol интерфейсы для определения контрактов (LLMClientProtocol, DialogManagerProtocol)
- **exceptions.py** - кастомные исключения (LLMAPIError, ConfigurationError)

### Поток данных

1. Пользователь → Telegram → Bot → MessageHandler
2. MessageHandler → DialogManager (получить историю)
3. MessageHandler → LLMClient (отправить сообщение + история)
4. LLMClient → Openrouter → LLM → ответ
5. MessageHandler → DialogManager (сохранить в историю)
6. MessageHandler → Bot → Telegram → Пользователь

## 5. Модель данных

### Класс Config

```python
class Config:
    """Конфигурация приложения из .env файла"""

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str

    # Openrouter/LLM
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENAI_MODEL: str = "openai/gpt-4"
    SYSTEM_PROMPT: str

    # Логирование
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/"

    # Контекст
    MAX_CONTEXT_MESSAGES: int = 0  # 0 = без ограничений
```

### Класс DialogManager

```python
class DialogManager:
    """Управление историей диалогов в памяти"""

    dialogs: dict[int, list[dict]]  # {user_id: [messages]}

    # Методы:
    # - get_history(user_id: int) -> list[dict]
    # - add_message(user_id: int, role: str, content: str) -> None
    # - clear_history(user_id: int) -> None
    # - _trim_history(history: list[dict]) -> list[dict]  # Обрезка контекста
```

**Примечание**: В будущем при рефакторинге планируется разделение на:
- `DialogRepository` - хранение данных
- `DialogContextService` - логика управления контекстом (обрезка истории)
- `DialogManager` - фасад над Repository и Service

### Формат сообщений (OpenAI API совместимый)

```python
Message = dict[str, str]  # {"role": "system|user|assistant", "content": "текст"}

# Пример истории диалога:
[
    {"role": "system", "content": "Ты помощник..."},
    {"role": "user", "content": "Привет"},
    {"role": "assistant", "content": "Привет! Как дела?"},
    {"role": "user", "content": "Хорошо"}
]
```

### Переменные окружения (.env файл)

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Openrouter/LLM
OPENAI_API_KEY=sk-or-v1-xxxxx
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4
SYSTEM_PROMPT=Ты полезный ассистент, который помогает пользователям

# Логирование
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/

# Контекст
MAX_CONTEXT_MESSAGES=0
```

### Особенности

- Системный промпт добавляется в начало истории при первом обращении пользователя
- История хранится в памяти (при перезапуске теряется)
- Ограничение длины истории через `MAX_CONTEXT_MESSAGES` (0 = без ограничений)
  - При обрезке сохраняется системный промпт + последние N*2 сообщений (пары user+assistant)

## 6. Работа с LLM

### Библиотека и провайдер

- **Библиотека**: `openai` (официальный Python клиент)
- **Провайдер**: Openrouter (OpenAI-совместимый API)
- **Base URL**: `https://openrouter.ai/api/v1`

### Интеграция в LLMClient

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url=config.OPENAI_BASE_URL,
    api_key=config.OPENAI_API_KEY
)

response = await client.chat.completions.create(
    model=config.OPENAI_MODEL,
    messages=dialog_history
)
```

### Параметры запроса

- `model` - из конфигурации (например, "openai/gpt-3.5-turbo")
- `messages` - полная история диалога с системным промптом
- Остальные параметры (temperature, max_tokens и т.д.) - по умолчанию

### Обработка ответа

- Извлечение текста: `response.choices[0].message.content`
- Обработка ошибок через try/except:
  - `OpenAIError` - ошибки API (неверный ключ, лимиты, недоступность)
  - `asyncio.TimeoutError` - таймауты сети
  - Логирование с `exc_info=True` для полного traceback
- При ошибке отправка пользователю сообщения "Произошла ошибка, попробуйте позже"

**Примечание**: В будущем планируется создание кастомного исключения `LLMAPIError` для унификации обработки ошибок API.

## 7. Сценарии работы

### Сценарий 1: Первое сообщение от пользователя

1. Пользователь отправляет `/start` или любое сообщение
2. MessageHandler валидирует входные данные (проверяет наличие текста)
3. Бот проверяет наличие истории для user_id
4. Если истории нет - создаёт новую, добавляет системный промпт
5. Добавляет сообщение пользователя в историю
6. Применяет обрезку контекста (если настроено MAX_CONTEXT_MESSAGES)
7. Отправляет историю в LLM
8. Получает ответ, добавляет в историю
9. Отправляет ответ пользователю

### Сценарий 2: Продолжение диалога

1. Пользователь отправляет сообщение
2. MessageHandler валидирует входные данные (проверяет наличие текста)
3. Бот получает существующую историю для user_id
4. Добавляет новое сообщение в историю
5. Применяет обрезку контекста (если настроено MAX_CONTEXT_MESSAGES)
6. Отправляет историю в LLM
7. Получает ответ, добавляет в историю
8. Отправляет ответ пользователю

### Сценарий 3: Команда /clear (очистка истории)

1. Пользователь отправляет `/clear`
2. Бот удаляет историю диалога для user_id
3. Отправляет подтверждение "История диалога очищена"

### Сценарий 4: Ошибка при обращении к LLM

1. При запросе к LLM возникает ошибка (OpenAIError, asyncio.TimeoutError)
2. LLMClient логирует ошибку с полным traceback
3. MessageHandler перехватывает исключение
4. Бот отправляет пользователю "Произошла ошибка, попробуйте позже"
5. История остаётся в состоянии до ошибки (сообщение пользователя сохранено, ответ ассистента не добавлен)

### Сценарий 5: Валидация входных данных

1. Пользователь отправляет сообщение без текста (например, только медиафайл)
2. MessageHandler проверяет наличие `message.text`
3. Если текста нет - обработчик завершается без действий (early return)
4. Бот не отвечает на сообщения без текста

## 8. Подход к конфигурированию

### Источник конфигурации

- **Файл**: `.env` в корне проекта
- **Библиотека**: `python-dotenv` для загрузки переменных окружения

### Обязательные параметры

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
OPENAI_API_KEY=sk-or-v1-xxxxx
SYSTEM_PROMPT=Ты полезный ассистент, который помогает пользователям
```

### Необязательные параметры (с дефолтами)

```env
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/
MAX_CONTEXT_MESSAGES=0
```

### Класс Config

- Загружает переменные через `os.getenv()`
- Проверяет наличие обязательных параметров при инициализации (Fail Fast)
- При отсутствии обязательного параметра - выбрасывает `ValueError` с понятным сообщением (в будущем - `ConfigurationError`)
- Хранит значения как атрибуты класса
- Конвертирует типы (например, `MAX_CONTEXT_MESSAGES` в int)

### Управление секретами

- `.env.example` - шаблон с примерами, добавляется в репозиторий
- `.env` - реальные значения, добавляется в `.gitignore`

## 9. Контроль качества кода

### Инструменты

- **ruff** - универсальный инструмент для форматирования и линтинга
  - Заменяет: black, flake8, isort, pyupgrade
  - Быстрый (написан на Rust)
  - Конфигурация в `pyproject.toml`

- **mypy** - статический анализатор типов
  - Проверяет type hints
  - Strict режим для максимальной безопасности
  - Конфигурация в `pyproject.toml`

- **pytest** - фреймворк для тестирования
  - Поддержка async через pytest-asyncio
  - Coverage через pytest-cov
  - Fixtures для переиспользования кода

### Makefile команды

```makefile
format:   # Автоформатирование кода (ruff format)
lint:     # Проверка качества (ruff check + mypy)
fix:      # Автоисправление простых ошибок (ruff --fix)
test:     # Запуск тестов (pytest)
test-cov: # Запуск тестов с coverage (pytest --cov)
run:      # Запуск бота
```

### Процесс разработки

1. Написать код
2. `make format` - отформатировать
3. `make lint` - проверить качество
4. `make test` - запустить тесты (если есть)
5. Коммит

### Метрики качества

- Линтер: 0 ошибок
- Type hints: 100% покрытие
- Tests: >= 80% для критичных компонентов

## 10. Подход к логгированию

### Библиотека

- **structlog** - структурированное логирование
- JSON формат для логов

### Уровни логирования

- **DEBUG** - детальная информация для отладки (параметры запросов к LLM, полная история)
- **INFO** - основные события (запуск бота, получение сообщения, отправка ответа)
- **WARNING** - предупреждения (длинная история диалога)
- **ERROR** - ошибки (проблемы с API, сетевые ошибки)

### Что логируем

- Запуск и остановка бота
- Входящие сообщения (user_id, текст сообщения)
- Запросы к LLM API (модель, количество сообщений в истории)
- Ответы от LLM (длина ответа)
- Ошибки с полным traceback

### Формат логов (JSON)

```json
{"event": "bot_started", "timestamp": "2024-10-10T15:30:45", "level": "info"}
{"event": "message_received", "user_id": 123456, "text": "Привет", "timestamp": "2024-10-10T15:31:12", "level": "info"}
{"event": "llm_request", "model": "gpt-3.5-turbo", "messages": 3, "timestamp": "2024-10-10T15:31:13", "level": "info"}
{"event": "llm_response", "length": 45, "timestamp": "2024-10-10T15:31:14", "level": "info"}
```

### Конфигурация

- Уровень логирования из `.env` (LOG_LEVEL)
- Путь к файлам логов из `.env` (LOG_FILE_PATH)
- Вывод в консоль (stdout) и в файл
- Ротация файлов логов

## 11. Подход к тестированию

### Стратегия

- **Unit-тесты**: для отдельных компонентов (Config, DialogManager, LLMClient)
- **Integration-тесты**: для взаимодействия компонентов (MessageHandler)
- **Mock-тесты**: для внешних API (использовать AsyncMock для async вызовов)

### Структура тестов

```python
tests/
├── conftest.py              # Общие fixtures
├── unit/                    # Изолированные тесты компонентов
│   ├── test_config.py
│   ├── test_dialog_manager.py
│   └── test_llm_client.py
└── integration/             # Тесты взаимодействия
    └── test_handler.py
```

### Fixtures

```python
@pytest.fixture
def config(monkeypatch):
    """Мокированная конфигурация"""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("SYSTEM_PROMPT", "test")
    return Config()

@pytest.fixture
def dialog_manager(config):
    """DialogManager с тестовой конфигурацией"""
    return DialogManager(config)
```

### Пример теста

```python
@pytest.mark.asyncio
async def test_llm_client_handles_api_error(llm_client, mock_openai):
    """Тест: LLMClient корректно обрабатывает ошибку API"""
    mock_openai.chat.completions.create.side_effect = OpenAIError("API Error")

    with pytest.raises(OpenAIError):
        await llm_client.generate_response([{"role": "user", "content": "Hi"}])
```

### Coverage

- Цель: >= 80% для src/
- Исключения: `__pycache__`, `tests/`
- Команда: `make test-cov`
