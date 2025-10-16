# Getting Started

Быстрый старт проекта за 10 минут.

## Prerequisites

- **Python 3.11+**
- **uv** - менеджер зависимостей ([установка](https://github.com/astral-sh/uv))
- **Git**
- **Telegram аккаунт** для создания бота

## Шаг 1: Клонирование

```bash
git clone <repository-url>
cd telegram-bot
```

## Шаг 2: Установка зависимостей

```bash
make install
```

Эта команда выполнит `uv sync` и установит все зависимости из `pyproject.toml`.

## Шаг 3: Настройка переменных окружения

### 3.1 Получить токен бота

1. Открыть [@BotFather](https://t.me/BotFather) в Telegram
2. Отправить `/newbot`
3. Следовать инструкциям
4. Скопировать токен (формат: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 3.2 Получить API ключ Openrouter

1. Зарегистрироваться на [openrouter.ai](https://openrouter.ai/)
2. Перейти в [Keys](https://openrouter.ai/keys)
3. Создать новый ключ
4. Скопировать ключ (формат: `sk-or-v1-xxxxx`)

### 3.3 Создать .env файл

```bash
# В корне проекта
cp .env.example .env
```

Заполнить `.env`:

```env
# Обязательные параметры
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
OPENAI_API_KEY=sk-or-v1-xxxxx
SYSTEM_PROMPT_FILE=prompts/music_consultant.txt

# Опциональные (уже есть дефолты)
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4
BOT_ROLE_NAME=Консультант по выбору музыки 🎵
BOT_ROLE_DESCRIPTION=Помогаю найти музыку по настроению, рекомендую треки и составляю плейлисты
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/
MAX_CONTEXT_MESSAGES=0
```

## Шаг 4: Запуск бота

```bash
make run
```

Вы должны увидеть:
```
{"event": "bot_started", "timestamp": "...", "level": "info", "model": "openai/gpt-4"}
Бот запущен...
```

## Шаг 5: Проверка работы

1. Открыть Telegram
2. Найти вашего бота по username
3. Отправить `/start`
4. Ожидаемый ответ: `Привет! Я LLM-ассистент`
5. Отправить любое сообщение, например: `Посоветуй музыку для работы`
6. Бот должен ответить в роли консультанта по музыке

## Команды бота

- `/start` - приветственное сообщение
- `/role` - показать роль и описание бота
- `/clear` - очистить историю диалога

## Troubleshooting

### Бот не запускается

**Ошибка**: `Обязательная переменная окружения TELEGRAM_BOT_TOKEN не установлена`

**Решение**: Проверить наличие `.env` файла и корректность токена

---

**Ошибка**: `Файл системного промпта не найден`

**Решение**: Проверить наличие `prompts/music_consultant.txt`

---

**Ошибка**: `OpenAIError: Invalid API key`

**Решение**: Проверить `OPENAI_API_KEY` в `.env`, убедиться что ключ активен на openrouter.ai

### Бот запустился но не отвечает

**Проблема**: Бот не реагирует на сообщения

**Решение**:
- Проверить что бот не заблокирован в Telegram
- Проверить логи в консоли на наличие ошибок
- Проверить баланс на openrouter.ai

### Как включить debug логи

В `.env` изменить:
```env
LOG_LEVEL=DEBUG
```

Перезапустить бота.

## Следующие шаги

- Прочитать [Architecture Overview](01_architecture_overview.md) для понимания структуры
- Изучить [Codebase Tour](02_codebase_tour.md) для навигации по коду
- Посмотреть [Configuration & Secrets](05_configuration_secrets.md) для тонкой настройки
