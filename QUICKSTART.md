# 🚀 Быстрый старт

Руководство по быстрому запуску Telegram Bot системы на сервере **89.223.67.136**.

## Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+
- SSH доступ к серверу 89.223.67.136

## Шаг 1: Подготовка

```bash
# Подключитесь к серверу
ssh root@89.223.67.136

# Клонируйте репозиторий
git clone <your-repo-url> /opt/telegram-bot
cd /opt/telegram-bot
```

## Шаг 2: Конфигурация

### Создайте .env файл

```bash
# Скопируйте пример
cp .env.example .env

# Или создайте вручную
cat > .env << 'EOF'
# Обязательные параметры
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here

# Порты
API_PORT=8004
FRONTEND_PORT=3004

# API URL для frontend
NEXT_PUBLIC_API_URL=http://89.223.67.136:8004

# Системный промпт
SYSTEM_PROMPT_FILE=prompts/music_consultant.txt

# Логирование
LOG_LEVEL=INFO
EOF
```

### Замените токены на реальные

```bash
# Отредактируйте .env файл
nano .env

# Обязательно укажите:
# - TELEGRAM_BOT_TOKEN (получите у @BotFather)
# - OPENAI_API_KEY (ваш OpenAI/OpenRouter API ключ)
```

## Шаг 3: Запуск

### Вариант A: Используя Makefile (рекомендуется)

```bash
# Для development (локальная сборка)
make dev-up

# Для production (образы из registry)
make prod-pull
make prod-up

# Проверка статуса
make status
make health
```

### Вариант B: Используя docker-compose напрямую

```bash
# Production режим
docker-compose pull
docker-compose up -d

# Development режим
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

## Шаг 4: Проверка

### Проверьте статус контейнеров

```bash
docker-compose ps
```

Ожидаемый результат:
```
NAME                  STATUS          PORTS
telegram-api          Up (healthy)    0.0.0.0:8004->8000/tcp
telegram-bot          Up (healthy)
telegram-frontend     Up (healthy)    0.0.0.0:3004->3000/tcp
```

### Проверьте работу сервисов

```bash
# API healthcheck
curl http://localhost:8004/health

# Frontend
curl http://localhost:3004

# Или используйте Makefile
make health
```

### Проверьте логи

```bash
# Все логи
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f bot
docker-compose logs -f api
docker-compose logs -f frontend

# Или используйте Makefile
make logs
make logs-api
```

## Шаг 5: Настройка Firewall

```bash
# Откройте необходимые порты
ufw allow 8004/tcp comment "Telegram Bot API"
ufw allow 3004/tcp comment "Telegram Bot Frontend"
ufw reload
```

## Доступ к сервисам

После успешного запуска сервисы доступны по адресам:

- **API**: http://89.223.67.136:8004
- **Frontend**: http://89.223.67.136:3004
- **API Health**: http://89.223.67.136:8004/health
- **API Docs**: http://89.223.67.136:8004/docs

## Полезные команды

```bash
# Просмотр статуса
make status

# Просмотр логов
make logs

# Перезапуск сервисов
make restart

# Проверка здоровья
make health

# Остановка
make down

# Резервное копирование БД
make db-backup

# Просмотр всех команд
make help
```

## Troubleshooting

### Проблема: Контейнеры не запускаются

```bash
# Проверьте логи
docker-compose logs

# Проверьте конфигурацию
docker-compose config

# Пересоздайте контейнеры
docker-compose up -d --force-recreate
```

### Проблема: API недоступен

```bash
# Проверьте статус
docker-compose ps api

# Проверьте логи
docker-compose logs api

# Проверьте порт
netstat -tulpn | grep 8004
```

### Проблема: Frontend не подключается к API

```bash
# Проверьте переменную окружения
docker-compose exec frontend env | grep API_URL

# Должно быть: NEXT_PUBLIC_API_URL=http://89.223.67.136:8004

# Если неправильно, исправьте в .env и пересоздайте контейнер
docker-compose up -d --force-recreate frontend
```

## Следующие шаги

1. ✅ Проверьте работу бота в Telegram
2. ✅ Откройте веб-интерфейс: http://89.223.67.136:3004
3. 📊 Настройте мониторинг (опционально)
4. 🔒 Настройте HTTPS через reverse proxy (рекомендуется)
5. 📋 Настройте автоматическое резервное копирование

## Дополнительная документация

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Полное руководство по развертыванию
- [Makefile](Makefile) - Все доступные команды
- [secrets/README.md](secrets/README.md) - Управление секретами
- [docs/guides/](docs/guides/) - Подробные руководства

## Получение помощи

Если возникли проблемы:

1. Проверьте логи: `make logs`
2. Проверьте конфигурацию: `docker-compose config`
3. Обратитесь к [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#troubleshooting)
4. Создайте issue в репозитории

---

**Готово! 🎉** Ваш Telegram Bot запущен и работает!
