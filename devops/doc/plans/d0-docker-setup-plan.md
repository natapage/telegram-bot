# План Спринта D0: Basic Docker Setup

## Обзор

Создать простую Docker-конфигурацию для локального запуска всех сервисов одной командой `docker-compose up`. Фокус на скорости и работоспособности, без преждевременной оптимизации.

## Сервисы

Проект состоит из 3 сервисов:

1. **Bot** - Telegram бот (Python + UV)
2. **API** - FastAPI сервер для дашборда (Python + UV)
3. **Frontend** - Next.js веб-интерфейс (pnpm)

**База данных**: SQLite (файл `telegram_bot.db` с volume для персистентности)

## Файлы для создания

### 1. Docker-образы

**`Dockerfile.bot`** - Telegram бот

- Базовый образ: `python:3.11-slim`
- Установка UV менеджера
- Копирование `pyproject.toml`, `uv.lock`
- Установка зависимостей через `uv sync`
- Копирование исходного кода `src/`
- Копирование промптов `prompts/`
- Копирование alembic для миграций
- Рабочая директория: `/app`
- Команда запуска: `uv run python -m src.main`

**`Dockerfile.api`** - FastAPI API

- Базовый образ: `python:3.11-slim`
- Установка UV менеджера
- Копирование `pyproject.toml`, `uv.lock`
- Установка зависимостей через `uv sync`
- Копирование исходного кода `src/`
- Копирование alembic для миграций
- Рабочая директория: `/app`
- Expose порт: 8000
- Команда запуска: `uv run python -m src.api_main`

**`Dockerfile.frontend`** - Next.js

- Базовый образ: `node:20-alpine`
- Установка pnpm глобально
- Копирование `package.json`, `pnpm-lock.yaml`
- Установка зависимостей: `pnpm install --frozen-lockfile`
- Копирование всей директории `frontend/`
- Рабочая директория: `/app`
- Expose порт: 3000
- Команда запуска: `pnpm dev` (для локальной разработки)

### 2. Docker Compose

**`docker-compose.yml`** - оркестрация сервисов

**Сервис `bot`:**

- Build: `Dockerfile.bot`
- Переменные окружения из файла `.env`
- Volumes:
  - `./prompts:/app/prompts:ro` (read-only для промптов)
  - `./telegram_bot.db:/app/telegram_bot.db` (SQLite база данных)
  - `./logs:/app/logs` (логи)
- Restart: `unless-stopped`
- Зависит от: `api`

**Сервис `api`:**

- Build: `Dockerfile.api`
- Порт: `8000:8000`
- Переменные окружения из файла `.env`
- Volumes:
  - `./telegram_bot.db:/app/telegram_bot.db` (SQLite база данных)
  - `./logs:/app/logs` (логи)
- Restart: `unless-stopped`

**Сервис `frontend`:**

- Build: `Dockerfile.frontend`
- Зависит от: `api`
- Порт: `3000:3000`
- Переменные окружения: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Restart: `unless-stopped`

### 3. Файлы исключений

**`.dockerignore`** (корневой) - для bot и api:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.venv/
venv/
.env
*.log
logs/
.git/
.gitignore
README.md
docs/
tests/
frontend/
*.db-journal
node_modules/
.dockerignore
Dockerfile*
docker-compose*.yml
.cursor/
devops/
doc/
```

**`frontend/.dockerignore`**:

```
node_modules/
.next/
out/
.git/
.gitignore
*.log
npm-debug.log*
.env*.local
.vercel
.turbo
coverage/
.vscode/
.idea/
*.swp
*.swo
README.md
tsconfig.tsbuildinfo
__tests__/
*.test.tsx
*.test.ts
vitest.config.ts
```

### 4. Конфигурация окружения

**`.env.example`** - шаблон переменных окружения:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenAI/LLM (Openrouter)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4

# System Prompt
SYSTEM_PROMPT_FILE=prompts/music_consultant.txt

# Bot Role
BOT_ROLE_NAME=ИИ-ассистент
BOT_ROLE_DESCRIPTION=Помогаю отвечать на вопросы

# Database (SQLite)
DATABASE_URL=sqlite+aiosqlite:///./telegram_bot.db

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/

# Context
MAX_CONTEXT_MESSAGES=10
```

### 5. Обновление Makefile

Добавлены новые команды для Docker:

```makefile
# Docker commands
.PHONY: docker-up docker-down docker-build docker-logs docker-status docker-clean

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build

docker-logs:
	docker-compose logs -f

docker-status:
	docker-compose ps

docker-clean:
	docker-compose down -v
	docker system prune -f
```

### 6. Документация

**Обновлен `README.md`** - добавлен раздел "Запуск через Docker":

- Быстрый старт: как создать .env и запустить сервисы
- Docker команды через Makefile
- Доступ к сервисам (порты и URLs)
- Применение миграций БД

## Порядок выполнения

1. ✅ Создать `.dockerignore` файлы (корневой и в `frontend/`)
2. ✅ Создать `Dockerfile.bot`
3. ✅ Создать `Dockerfile.api`
4. ✅ Создать `Dockerfile.frontend`
5. ✅ Создать `docker-compose.yml`
6. ✅ Создать `.env.example`
7. ✅ Обновить `Makefile` (добавить Docker команды)
8. ✅ Обновить `README.md` (добавить раздел Docker)
9. ✅ Создать файл плана `devops/doc/plans/d0-docker-setup-plan.md`
10. ⏳ Обновить статус в `devops/doc/devops-roadmap.md`

## Проверка работоспособности

После выполнения плана:

1. Создать `.env` из `.env.example` и заполнить токены:
   ```bash
   cp .env.example .env
   # Отредактировать .env, добавить токены
   ```

2. Запустить сборку и запуск:
   ```bash
   make docker-build
   make docker-up
   ```

3. Проверить статус:
   ```bash
   make docker-status
   ```
   Все 3 сервиса должны быть в состоянии "running"

4. Применить миграции (если БД пустая):
   ```bash
   docker-compose exec api uv run alembic upgrade head
   ```

5. Проверить логи:
   ```bash
   make docker-logs
   ```

6. Проверить сервисы:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

7. Проверить работу бота в Telegram

## Технические детали

- **База данных**: SQLite с файлом `telegram_bot.db` (монтируется через volume)
- **Драйвер**: `aiosqlite` для асинхронной работы с SQLite (уже в зависимостях)
- **Порты**: 3000 (frontend), 8000 (api)
- **Volumes**:
  - `./telegram_bot.db:/app/telegram_bot.db` - персистентность БД
  - `./prompts:/app/prompts:ro` - промпты (read-only)
  - `./logs:/app/logs` - логи
- **Restart policy**: `unless-stopped` для всех сервисов
- **Network**: default bridge network (автоматически создается docker-compose)
- **Зависимости**: bot зависит от api, frontend зависит от api

## Ограничения MVP

В этом спринте НЕ делаем:

- Multi-stage builds
- Оптимизацию размера образов
- Hadolint проверки
- Production-ready конфигурацию
- Secrets management (используем .env файл)
- PostgreSQL (используем SQLite для простоты)
- Мониторинг и метрики

Все это будет добавлено в следующих спринтах по мере необходимости.

## Результаты

Спринт D0 выполнен успешно! Теперь все сервисы можно запустить одной командой:

```bash
make docker-up
```

Проект готов к локальной разработке и тестированию через Docker.
