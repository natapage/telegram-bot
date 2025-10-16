# Configuration & Secrets

Управление конфигурацией и секретами.

## Структура конфигурации

```mermaid
flowchart LR
    ENV[.env file] --> DotEnv[python-dotenv]
    DotEnv --> OS[os.getenv]
    OS --> Config[Config class]
    Config --> App[Application]

    Example[.env.example] -.->|template| ENV

    style ENV fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style Config fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
    style Example fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
```

## Файл .env

### Расположение

Корень проекта: `telegram-bot/.env`

### Создание

```bash
cp .env.example .env
```

Затем отредактировать значения.

### Структура

```env
# ============================================
# Telegram Bot (Обязательно)
# ============================================
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# ============================================
# Openrouter/LLM (Обязательно)
# ============================================
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxx

# Провайдер (опционально, default: openrouter)
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Модель (опционально, default: openai/gpt-4)
OPENAI_MODEL=openai/gpt-4

# ============================================
# System Prompt (Обязательно одно из двух)
# ============================================
# Вариант 1: из файла (рекомендуется)
SYSTEM_PROMPT_FILE=prompts/music_consultant.txt

# Вариант 2: напрямую в env (если файла нет)
# SYSTEM_PROMPT=Ты эксперт-консультант...

# ============================================
# Bot роль (опционально)
# ============================================
BOT_ROLE_NAME=Консультант по выбору музыки 🎵
BOT_ROLE_DESCRIPTION=Помогаю найти музыку по настроению, рекомендую треки и составляю плейлисты

# ============================================
# Logging (опционально)
# ============================================
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/

# ============================================
# Context (опционально)
# ============================================
# 0 = без ограничений (хранить всю историю)
# N = хранить системный промпт + последние N*2 сообщений
MAX_CONTEXT_MESSAGES=0
```

### Важно: .env в .gitignore

```gitignore
.env
```

**Никогда не коммитить** `.env` с реальными секретами в репозиторий!

## Параметры конфигурации

### Обязательные параметры

| Параметр | Описание | Где получить |
|----------|----------|--------------|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | [@BotFather](https://t.me/BotFather) |
| `OPENAI_API_KEY` | API ключ провайдера | [openrouter.ai/keys](https://openrouter.ai/keys) |
| `SYSTEM_PROMPT_FILE` или `SYSTEM_PROMPT` | Системный промпт | Файл или строка |

**Если отсутствуют**: `ValueError` при запуске бота.

### Опциональные параметры (с дефолтами)

| Параметр | Default | Описание |
|----------|---------|----------|
| `OPENAI_BASE_URL` | `https://openrouter.ai/api/v1` | URL API провайдера |
| `OPENAI_MODEL` | `openai/gpt-4` | Модель LLM |
| `BOT_ROLE_NAME` | `ИИ-ассистент` | Название роли для `/role` |
| `BOT_ROLE_DESCRIPTION` | `Помогаю отвечать на вопросы` | Описание роли |
| `LOG_LEVEL` | `INFO` | Уровень логирования |
| `LOG_FILE_PATH` | `logs/` | Директория для логов |
| `MAX_CONTEXT_MESSAGES` | `0` | Ограничение контекста (0 = без ограничений) |

## Получение секретов

### Telegram Bot Token

**Шаги**:
1. Открыть [@BotFather](https://t.me/BotFather) в Telegram
2. Отправить `/newbot`
3. Указать имя бота: `My Music Bot`
4. Указать username: `my_music_bot` (должен заканчиваться на `bot`)
5. Скопировать токен из сообщения

**Формат токена**: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

**Проверка**: Отправить GET запрос:
```bash
curl https://api.telegram.org/bot<TOKEN>/getMe
```

### Openrouter API Key

**Шаги**:
1. Зарегистрироваться на https://openrouter.ai/
2. Перейти в раздел [Keys](https://openrouter.ai/keys)
3. Нажать "Create Key"
4. Скопировать ключ (показывается один раз!)

**Формат ключа**: `sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Первый запуск**: Дается бесплатный кредит для тестирования

**Пополнение баланса**: https://openrouter.ai/credits

## Системный промпт

### Вариант 1: Из файла (рекомендуется)

**В .env**:
```env
SYSTEM_PROMPT_FILE=prompts/music_consultant.txt
```

**Преимущества**:
- Легко редактировать (обычный текстовый файл)
- Можно использовать многострочный текст
- Версионируется в Git
- Можно создать несколько промптов для разных ролей

**Создание нового промпта**:
```bash
# Создать новый файл
echo "Ты эксперт в..." > prompts/my_role.txt

# Изменить .env
SYSTEM_PROMPT_FILE=prompts/my_role.txt
```

### Вариант 2: Напрямую в .env

**В .env**:
```env
SYSTEM_PROMPT=Ты эксперт-консультант по музыке. Помогаешь подбирать треки и составлять плейлисты.
```

**Когда использовать**:
- Короткий промпт
- Нужна динамическая генерация (CI/CD)

**Недостатки**:
- Сложно редактировать длинные промпты
- Проблемы с переносами строк

### Логика загрузки

```python
# src/config.py
def _load_system_prompt(self) -> str:
    # 1. Попытка загрузить из файла
    prompt_file = os.getenv("SYSTEM_PROMPT_FILE")
    if prompt_file:
        with open(prompt_file, encoding="utf-8") as f:
            return f.read().strip()

    # 2. Fallback на переменную окружения
    prompt = os.getenv("SYSTEM_PROMPT")
    if prompt:
        return prompt

    # 3. Если ничего не настроено - ошибка
    raise ValueError("Системный промпт не настроен")
```

## Смена модели LLM

### Доступные модели

**Openrouter**: https://openrouter.ai/models

**Популярные модели**:
- `openai/gpt-4` - сильная, дорогая
- `openai/gpt-3.5-turbo` - быстрая, дешевая
- `anthropic/claude-3-sonnet` - Claude от Anthropic
- `google/gemini-pro` - Gemini от Google
- `meta-llama/llama-3-70b-instruct` - open source

### Изменение модели

**В .env**:
```env
OPENAI_MODEL=openai/gpt-3.5-turbo
```

Перезапустить бота.

**Проверка в логах**:
```json
{"event":"bot_started","model":"openai/gpt-3.5-turbo",...}
```

## Переключение провайдера

### С Openrouter на OpenAI

**В .env**:
```env
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-proj-xxxxx  # ключ от OpenAI
OPENAI_MODEL=gpt-4
```

### С Openrouter на Anthropic

**В .env**:
```env
OPENAI_BASE_URL=https://api.anthropic.com/v1
OPENAI_API_KEY=sk-ant-xxxxx  # ключ от Anthropic
OPENAI_MODEL=claude-3-sonnet-20240229
```

**Важно**: API должен быть OpenAI-совместимым.

## Управление контекстом

### MAX_CONTEXT_MESSAGES

**Что делает**: Ограничивает количество сообщений в истории диалога.

**Значения**:
- `0` (default) - без ограничений, хранить всю историю
- `N` - хранить системный промпт + последние N*2 сообщений

**Примеры**:
```env
MAX_CONTEXT_MESSAGES=0   # Вся история
MAX_CONTEXT_MESSAGES=5   # system + 10 сообщений (5 пар user+assistant)
MAX_CONTEXT_MESSAGES=10  # system + 20 сообщений
```

**Когда использовать**:
- Длинные диалоги → большой расход токенов
- Ограниченный бюджет API
- Модель с малым context window

## Логирование

### LOG_LEVEL

**Значения**:
- `DEBUG` - максимальная детализация
- `INFO` - основные события (default)
- `WARNING` - предупреждения
- `ERROR` - только ошибки

**Когда менять**:
```env
# Разработка - детальные логи
LOG_LEVEL=DEBUG

# Production - только важные события
LOG_LEVEL=INFO
```

### LOG_FILE_PATH

**Default**: `logs/`

Директория создается автоматически при запуске.

**Изменение**:
```env
LOG_FILE_PATH=/var/log/telegram-bot/
```

## Best Practices

### Безопасность

✅ **Делать**:
- Хранить `.env` локально, не коммитить
- Использовать `.env.example` для шаблона (без секретов)
- Ротировать API ключи периодически

❌ **Не делать**:
- Коммитить `.env` в Git
- Хардкодить токены в коде
- Публиковать ключи в issues/PR

### Окружения (dev/staging/prod)

**Подход**: разные `.env` файлы

```bash
.env.dev
.env.staging
.env.prod
```

**Запуск с конкретным env**:
```bash
cp .env.dev .env
make run
```

### Валидация конфигурации

**Текущая реализация**:
```python
# src/config.py
def _get_required(self, key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Обязательная переменная {key} не установлена")
    return value
```

**Fail Fast**: Бот не запустится если конфигурация неверная.

## Добавление нового параметра

### Шаги

1. **Обновить Config**:
```python
# src/config.py
self.NEW_PARAM: str = os.getenv("NEW_PARAM", "default_value")
```

2. **Обновить .env.example**:
```env
# New Feature
NEW_PARAM=example_value
```

3. **Обновить документацию** (этот файл, vision.md)

4. **Добавить тест**:
```python
# tests/unit/test_config.py
def test_config_loads_new_param(monkeypatch):
    monkeypatch.setenv("NEW_PARAM", "test_value")
    config = Config()
    assert config.NEW_PARAM == "test_value"
```

## Следующие шаги

- Изучить [Development Workflow](06_development_workflow.md) для разработки с конфигурацией
- Прочитать [Testing Guide](07_testing_guide.md) для мокирования конфигурации в тестах
- Посмотреть [Troubleshooting](10_troubleshooting.md) для решения проблем с конфигурацией
