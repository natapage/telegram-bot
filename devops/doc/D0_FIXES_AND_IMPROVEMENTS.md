# Исправления и улучшения после тестирования D0

**Дата**: 18 октября 2025

## Обзор

После тестирования Docker setup были выявлены и исправлены 3 проблемы. Все сервисы теперь работают корректно.

## Исправления

### 1. Dockerfile.frontend - Build Context

**Проблема**:
```
failed to calculate checksum of ref: "/frontend": not found
```

**Причина**:
- Build context был установлен как корень проекта (`.`)
- В `.dockerignore` была исключена директория `frontend/`
- Docker не мог найти файлы для копирования

**Решение в `docker-compose.yml`**:
```yaml
# Было:
frontend:
  build:
    context: .
    dockerfile: Dockerfile.frontend

# Стало:
frontend:
  build:
    context: ./frontend
    dockerfile: ../Dockerfile.frontend
```

**Решение в `Dockerfile.frontend`**:
```dockerfile
# Было:
COPY frontend/package.json ./package.json
COPY frontend/pnpm-lock.yaml ./pnpm-lock.yaml
COPY frontend/ ./

# Стало:
COPY package.json pnpm-lock.yaml ./
COPY . ./
```

### 2. Конфликт портов Frontend

**Проблема**:
```
ports are not available: exposing port TCP 0.0.0.0:3000 -> 127.0.0.1:0: bind:
Only one usage of each socket address is normally permitted.
```

**Причина**:
- Локальный Next.js dev server уже работает на порту 3000

**Решение в `docker-compose.yml`**:
```yaml
# Было:
frontend:
  ports:
    - "3000:3000"

# Стало:
frontend:
  ports:
    - "3001:3000"
```

**Доступ**: Frontend теперь доступен на http://localhost:3001

### 3. API не находит промпт-файл

**Проблема**:
```
ValueError: Файл системного промпта не найден: prompts/music_consultant.txt
```

**Причина**:
- У API сервиса не был настроен volume с промптами
- Bot сервис имел volume с промптами, но API - нет

**Решение в `docker-compose.yml`**:
```yaml
# Было:
api:
  volumes:
    - ./telegram_bot.db:/app/telegram_bot.db
    - ./logs:/app/logs

# Стало:
api:
  volumes:
    - ./prompts:/app/prompts:ro
    - ./telegram_bot.db:/app/telegram_bot.db
    - ./logs:/app/logs
```

## Улучшения

### 4. Удаление устаревшего атрибута version

**Изменение в `docker-compose.yml`**:
```yaml
# Было:
version: '3.8'

services:
  ...

# Стало:
services:
  ...
```

**Причина**: Атрибут `version` устарел и вызывал warning в Docker Compose v2.

## Итоговая конфигурация

### docker-compose.yml (финальная версия)

```yaml
services:
  # Telegram Bot
  bot:
    build:
      context: .
      dockerfile: Dockerfile.bot
    container_name: telegram-bot
    env_file:
      - .env
    volumes:
      - ./prompts:/app/prompts:ro
      - ./telegram_bot.db:/app/telegram_bot.db
      - ./logs:/app/logs
    restart: unless-stopped
    depends_on:
      - api

  # FastAPI Backend
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: telegram-api
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./prompts:/app/prompts:ro
      - ./telegram_bot.db:/app/telegram_bot.db
      - ./logs:/app/logs
    restart: unless-stopped

  # Next.js Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: ../Dockerfile.frontend
    container_name: telegram-frontend
    ports:
      - "3001:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    restart: unless-stopped
    depends_on:
      - api
```

### Dockerfile.frontend (финальная версия)

```dockerfile
# Dockerfile для Next.js фронтенда
FROM node:20-alpine

# Установка pnpm глобально
RUN npm install -g pnpm

# Рабочая директория
WORKDIR /app

# Копирование package.json и pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Установка зависимостей
RUN pnpm install --frozen-lockfile

# Копирование остальных файлов проекта
COPY . ./

# Expose порта
EXPOSE 3000

# Запуск в dev режиме для локальной разработки
CMD ["pnpm", "dev"]
```

## Проверка работоспособности

### Статус контейнеров

```bash
$ docker-compose ps

NAME                IMAGE                   STATUS         PORTS
telegram-api        telegram-bot-api        Up 2 minutes   0.0.0.0:8000->8000/tcp
telegram-bot        telegram-bot-bot        Up 4 minutes
telegram-frontend   telegram-bot-frontend   Up 3 minutes   0.0.0.0:3001->3000/tcp
```

✅ Все сервисы работают

### Health Checks

**API**:
```bash
$ curl http://localhost:8000/health
{"status":"ok","service":"dashboard-api"}
```
✅ Работает

**Frontend**:
```bash
$ curl http://localhost:3001
<title>Telegram Bot Dashboard</title>
...
```
✅ Работает

**Bot**:
```
{"model": "openai/gpt-3.5-turbo", "event": "bot_started", "level": "info"}
```
✅ Работает

## Обновленная документация

Файлы были обновлены с учетом изменений:

- ✅ `docker-compose.yml` - исправлены все проблемы
- ✅ `Dockerfile.frontend` - правильные пути
- ✅ `README.md` - обновлен порт frontend (3001)
- ✅ `SPRINT_D0_SUMMARY.md` - добавлена секция тестирования
- ✅ `devops/doc/reports/d0-testing-report.md` - детальный отчет

## Итог

Все найденные проблемы исправлены. Docker setup полностью функционален и готов к использованию.

**Статус**: ✅ Работает стабильно

**Время исправления**: ~10 минут

**Готовность для разработки**: 100%
