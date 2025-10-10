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
- Без тестов на начальном этапе (добавим позже при необходимости)
- Рефакторинг только по необходимости

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
│   └── config.py            # Класс Config - конфигурация
├── docs/
│   ├── idea.md              # Идея проекта
│   ├── vision.md            # Техническое видение
│   ├── conventions.md       # Правила разработки кода
│   ├── tasklist.md          # План разработки
│   └── workflow.md          # Процесс выполнения работ
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
- Документация в директории `docs/`
- Конфигурация через `.env` файл

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
3. **MessageHandler** - получает сообщения от пользователей, взаимодействует с DialogManager и LLMClient, отправляет ответы
4. **DialogManager** - хранит историю диалогов в словаре `{user_id: [messages]}`
5. **LLMClient** - формирует запрос к LLM, отправляет через openai client к Openrouter, возвращает ответ
6. **Config** - загружает переменные из .env (TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, SYSTEM_PROMPT, OPENAI_MODEL)

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
```

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
- Без ограничений на длину истории

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
- Простая обработка ошибок через try/except
- При ошибке отправка пользователю сообщения "Произошла ошибка, попробуйте позже"

## 7. Сценарии работы

### Сценарий 1: Первое сообщение от пользователя

1. Пользователь отправляет `/start` или любое сообщение
2. Бот проверяет наличие истории для user_id
3. Если истории нет - создаёт новую, добавляет системный промпт
4. Добавляет сообщение пользователя в историю
5. Отправляет историю в LLM
6. Получает ответ, добавляет в историю
7. Отправляет ответ пользователю

### Сценарий 2: Продолжение диалога

1. Пользователь отправляет сообщение
2. Бот получает существующую историю для user_id
3. Добавляет новое сообщение в историю
4. Отправляет историю в LLM
5. Получает ответ, добавляет в историю
6. Отправляет ответ пользователю

### Сценарий 3: Команда /clear (очистка истории)

1. Пользователь отправляет `/clear`
2. Бот удаляет историю диалога для user_id
3. Отправляет подтверждение "История диалога очищена"

### Сценарий 4: Ошибка при обращении к LLM

1. При запросе к LLM возникает ошибка (сеть, API и т.д.)
2. Бот отправляет пользователю "Произошла ошибка, попробуйте позже"
3. История не изменяется

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
- Проверяет наличие обязательных параметров при инициализации
- При отсутствии обязательного параметра - выбрасывает исключение с понятным сообщением
- Хранит значения как атрибуты класса

### Управление секретами

- `.env.example` - шаблон с примерами, добавляется в репозиторий
- `.env` - реальные значения, добавляется в `.gitignore`

## 9. Подход к логгированию

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
