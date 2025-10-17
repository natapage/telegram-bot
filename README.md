# LLM-ассистент Telegram-бот

LLM-ассистент, реализованный в виде Telegram-бота для взаимодействия с пользователями.

## Описание

Бот ведет диалог с пользователем и отвечает на вопросы, используя заданную роль из системного промпта LLM через Openrouter.

### Компоненты проекта

- **Backend** (Telegram Bot) - основная логика бота для взаимодействия в Telegram
- **Frontend** (в разработке) - веб-интерфейс с дашбордом статистики и ИИ-чатом
  - См. [Frontend Roadmap](doc/frontend-roadmap.md) для плана развития

## Установка

1. Клонировать репозиторий
2. Установить зависимости:
```bash
make install
```

## Настройка

1. Скопировать `.env.example` в `.env`
2. Заполнить переменные окружения:
   - `TELEGRAM_BOT_TOKEN` - токен от @BotFather
   - `OPENAI_API_KEY` - ключ API от Openrouter
   - `SYSTEM_PROMPT_FILE` - путь к файлу с системным промптом (например, `prompts/music_consultant.txt`)
   - `DATABASE_URL` - URL базы данных (по умолчанию: `sqlite+aiosqlite:///./telegram_bot.db`)

3. Применить миграции базы данных:
```bash
uv run alembic upgrade head
```

## Запуск

```bash
make run
```

## Команды бота

- `/start` - начать диалог
- `/role` - показать роль и описание бота
- `/clear` - очистить историю диалога (soft delete)

## База данных

Проект использует SQLite для персистентного хранения истории диалогов.

### Управление миграциями

```bash
# Применить все миграции
uv run alembic upgrade head

# Откатить последнюю миграцию
uv run alembic downgrade -1

# Посмотреть текущее состояние
uv run alembic current

# Создать новую миграцию
uv run alembic revision -m "описание"
```

### Особенности

- **Soft delete**: данные не удаляются физически, помечаются флагом `is_deleted`
- **Персистентность**: история сохраняется между перезапусками
- **Метаданные**: каждое сообщение имеет `created_at` и `length` (длина в символах)

Подробнее: [Data Model Guide](docs/guides/03_data_model.md)

## Документация

### 🚀 Быстрый старт

Новичкам рекомендуется начать с:
1. **[Getting Started](docs/guides/00_getting_started.md)** - детальная инструкция по установке и первому запуску
2. **[Architecture Overview](docs/guides/01_architecture_overview.md)** - понимание архитектуры проекта

### 📚 Полная документация

**[Все гайды](docs/guides/README.md)** - 12 подробных гайдов по всем аспектам проекта:

- **Основы**: Getting Started, Architecture, Codebase Tour
- **Технические детали**: Data Model, Integrations, Configuration
- **Разработка**: Development Workflow, Testing, Code Review
- **Операции**: CI/CD, Troubleshooting, Extending

### 📖 Дополнительно

- **[vision.md](docs/vision.md)** - техническое видение и архитектура backend
- **[roadmap.md](docs/roadmap.md)** - roadmap backend проекта по спринтам
- **[frontend-roadmap.md](doc/frontend-roadmap.md)** - roadmap frontend проекта (дашборд и веб-чат)
- **[tasklists/](docs/tasklists/)** - детальные планы работ по спринтам

## Разработка

### Makefile команды

#### Основные команды

```bash
make install    # установка зависимостей
make run        # запуск Telegram бота
make format     # автоформатирование
make lint       # проверка качества (ruff + mypy)
make test       # запуск тестов
make test-cov   # тесты + coverage
```

#### Frontend Mock API

```bash
make run-api    # запуск Mock API для дашборда (http://localhost:8000)
make test-api   # тестирование API endpoints
make api-docs   # показать ссылки на API документацию
```

Подробнее: [Mock API Documentation](doc/api-examples.md)

### Перед коммитом

```bash
make format && make lint && make test
```
