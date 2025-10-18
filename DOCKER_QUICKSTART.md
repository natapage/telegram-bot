# Docker Quick Start

Быстрая инструкция по запуску проекта через Docker.

## Предварительные требования

- Docker и Docker Compose установлены
- Токен Telegram бота (от @BotFather)
- API ключ от Openrouter

## Шаги запуска

### 1. Создать конфигурацию

```bash
cp .env.example .env
```

Отредактировать `.env` и заполнить:
- `TELEGRAM_BOT_TOKEN` - ваш токен от @BotFather
- `OPENAI_API_KEY` - ваш ключ от Openrouter

### 2. Запустить сервисы

```bash
make docker-build
make docker-up
```

Или напрямую:
```bash
docker-compose build
docker-compose up -d
```

### 3. Применить миграции БД (при первом запуске)

```bash
docker-compose exec api uv run alembic upgrade head
```

### 4. Проверить статус

```bash
make docker-status
```

Все 3 сервиса должны быть в состоянии "Up":
- telegram-bot
- telegram-api
- telegram-frontend

### 5. Проверить логи

```bash
make docker-logs
```

Или для конкретного сервиса:
```bash
docker-compose logs -f bot
docker-compose logs -f api
docker-compose logs -f frontend
```

### 6. Открыть сервисы

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Telegram Bot**: отправьте `/start` боту в Telegram

## Полезные команды

```bash
# Остановить все сервисы
make docker-down

# Пересобрать образы
make docker-build

# Посмотреть логи
make docker-logs

# Статус сервисов
make docker-status

# Полная очистка (удалить volumes и images)
make docker-clean
```

## Решение проблем

### Сервис не запускается

Проверьте логи:
```bash
docker-compose logs <service-name>
```

### Ошибка подключения к БД

Убедитесь, что файл `telegram_bot.db` существует и доступен для записи.

### Порт уже занят

Если порты 3000 или 8000 заняты другими приложениями, измените их в `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # для frontend
  - "8001:8000"  # для api
```

## Остановка

```bash
make docker-down
```

Это остановит все контейнеры, но сохранит данные БД и логи.

## Полная очистка

```bash
make docker-clean
```

**Внимание**: это удалит все данные, включая БД и логи!
