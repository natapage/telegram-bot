# 🐳 Docker Orchestration - Документация

Полная документация по системе оркестрации Telegram Bot с использованием Docker Compose.

## 📋 Содержание

- [Обзор системы](#обзор-системы)
- [Структура файлов](#структура-файлов)
- [Сервисы](#сервисы)
- [Конфигурационные файлы](#конфигурационные-файлы)
- [Быстрый старт](#быстрый-старт)
- [Сценарии использования](#сценарии-использования)

---

## 🎯 Обзор системы

Система состоит из трех основных сервисов:

1. **Bot** - Telegram бот для взаимодействия с пользователями
2. **API** - FastAPI backend для обработки запросов и работы с данными
3. **Frontend** - Next.js веб-интерфейс для управления и аналитики

### Серверная конфигурация

- **Сервер**: 89.223.67.136
- **API порт**: 8004 (внутренний: 8000)
- **Frontend порт**: 3004 (внутренний: 3000)
- **База данных**: SQLite (монтируется как volume)

---

## 📁 Структура файлов

### Docker Compose файлы

```
.
├── docker-compose.yml              # Основной файл оркестрации (production-ready)
├── docker-compose.prod.yml         # Production overrides
├── docker-compose.dev.yml          # Development overrides
└── docker-compose.registry.yml     # Упрощенная версия для быстрого старта
```

### Конфигурационные файлы

```
.
├── ENV_EXAMPLE.txt                 # Пример переменных окружения (для Windows)
├── .env                           # Файл с переменными окружения (создается из примера)
├── .dockerignore                  # Исключения для Docker build
└── .gitignore                     # Обновлен для secrets и backups
```

### Документация

```
.
├── QUICKSTART.md                  # Быстрый старт (5 минут)
├── DEPLOYMENT_GUIDE.md            # Полное руководство по развертыванию
├── DOCKER_ORCHESTRATION_README.md # Этот файл
└── Makefile                       # Утилиты для управления системой
```

### Secrets

```
secrets/
├── .gitkeep
├── README.md                      # Документация по управлению секретами
├── telegram_bot_token.txt         # Токен бота (создается вручную)
└── openai_api_key.txt            # API ключ (создается вручную)
```

---

## 🎛️ Сервисы

### 1. Bot Service

```yaml
Образ: ghcr.io/natapage/bot:latest
Зависимости: api (с healthcheck)
Restart: unless-stopped
Volumes:
  - prompts (read-only)
  - bot-data (база данных)
  - bot-logs
Resources:
  CPU: 0.25-1.0
  Memory: 128M-512M
Healthcheck: Python check (30s interval)
```

### 2. API Service

```yaml
Образ: ghcr.io/natapage/api:latest
Порты: 8004:8000
Restart: unless-stopped
Volumes:
  - prompts (read-only)
  - api-data (база данных)
  - api-logs
Resources:
  CPU: 0.5-2.0
  Memory: 256M-1G
Healthcheck: /health endpoint (30s interval)
```

### 3. Frontend Service

```yaml
Образ: ghcr.io/natapage/frontend:latest
Порты: 3004:3000
Зависимости: api (с healthcheck)
Restart: unless-stopped
Environment:
  - NEXT_PUBLIC_API_URL=http://89.223.67.136:8004
Resources:
  CPU: 0.25-1.0
  Memory: 128M-512M
Healthcheck: Root endpoint (30s interval)
```

### Volumes

| Volume    | Назначение                | Backup | Путь в контейнере      |
|-----------|---------------------------|--------|------------------------|
| bot-data  | База данных (bot)         | ✅     | /app/data              |
| api-data  | База данных (api)         | ✅     | /app/data              |
| bot-logs  | Логи бота                 | ❌     | /app/logs              |
| api-logs  | Логи API                  | ❌     | /app/logs              |
| prompts   | Системные промпты (bind)  | ✅     | /app/prompts           |

### Network

- **Имя**: telegram-network
- **Драйвер**: bridge
- **Подсеть**: 172.28.0.0/16
- **Изоляция**: Dedicated network для безопасности

---

## ⚙️ Конфигурационные файлы

### docker-compose.yml

Основной файл оркестрации. Использует образы из GitHub Container Registry.

**Особенности:**
- Named volumes для персистентности
- Dedicated network для изоляции
- Resource limits (CPU, Memory)
- Healthchecks для всех сервисов
- Structured logging (JSON с rotation)
- Depends_on с условием healthy

**Использование:**
```bash
docker-compose up -d
```

### docker-compose.prod.yml

Production overrides - дополнительные настройки для production.

**Особенности:**
- Версионирование образов (BOT_VERSION, API_VERSION)
- Более строгие resource limits
- Расширенное логирование (50MB, 10 файлов)
- Docker secrets support
- Restart policies с backoff
- Production healthchecks (1 минута)

**Использование:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### docker-compose.dev.yml

Development overrides - для локальной разработки.

**Особенности:**
- Локальная сборка образов (build вместо pull)
- Hot reload (монтирование исходников)
- Debug ports (5678 для Python, 9229 для Node)
- Более частые healthchecks (10s)
- Меньше ограничений по ресурсам
- Debug environment variables

**Использование:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### docker-compose.registry.yml

Упрощенная версия для быстрого старта.

**Особенности:**
- Минимальная конфигурация
- Прямое монтирование локальной БД
- Без resource limits
- Базовые healthchecks

**Использование:**
```bash
docker-compose -f docker-compose.registry.yml up -d
```

---

## 🚀 Быстрый старт

### Вариант 1: С использованием Makefile (рекомендуется)

```bash
# 1. Создайте .env файл
make env-example
# Отредактируйте .env и заполните токены

# 2. Для development
make dev-up

# 3. Для production
make prod-pull
make prod-up

# 4. Проверка
make status
make health
```

### Вариант 2: Прямое использование Docker Compose

```bash
# 1. Создайте .env файл из примера
cp ENV_EXAMPLE.txt .env
# Отредактируйте .env

# 2. Запустите систему
docker-compose up -d

# 3. Проверка
docker-compose ps
curl http://localhost:8004/health
```

### Вариант 3: Быстрый старт (registry version)

```bash
# 1. Создайте .env
cp ENV_EXAMPLE.txt .env
# Отредактируйте .env

# 2. Запустите
docker-compose -f docker-compose.registry.yml up -d
```

---

## 📚 Сценарии использования

### 1. Первоначальное развертывание на сервере

```bash
# Подключение к серверу
ssh root@89.223.67.136

# Клонирование
git clone <repo> /opt/telegram-bot
cd /opt/telegram-bot

# Конфигурация
cp ENV_EXAMPLE.txt .env
nano .env  # Заполните токены

# Запуск production
docker-compose pull
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Проверка
docker-compose ps
curl http://localhost:8004/health
```

### 2. Локальная разработка

```bash
# Клонирование
git clone <repo>
cd telegram-bot

# Конфигурация
cp ENV_EXAMPLE.txt .env
nano .env

# Сборка и запуск
make dev-build
make dev-up

# Логи
make dev-logs
```

### 3. Обновление production системы

```bash
# Подключение к серверу
ssh root@89.223.67.136
cd /opt/telegram-bot

# Backup базы данных
make db-backup

# Pull новых образов
make prod-pull

# Обновление
make prod-update

# Проверка
make health
make logs-api
```

### 4. Откат к предыдущей версии

```bash
# Остановка
docker-compose down

# Указание версий в .env
echo "BOT_VERSION=v1.0.0" >> .env
echo "API_VERSION=v1.0.0" >> .env
echo "FRONTEND_VERSION=v1.0.0" >> .env

# Запуск
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 5. Резервное копирование и восстановление

```bash
# Резервное копирование
make db-backup

# Список бэкапов
make db-list-backups

# Восстановление
make db-restore FILE=backups/telegram_bot_20240101.db
```

### 6. Мониторинг и отладка

```bash
# Статус всех сервисов
make status

# Здоровье сервисов
make health

# Логи
make logs           # Все сервисы
make logs-api       # Только API
make logs-bot       # Только бот

# Статистика ресурсов
make stats

# Shell в контейнере
make shell-api
make shell-bot
```

### 7. Production с секретами

```bash
# Создание структуры
make secrets-setup

# Заполнение секретов
echo "your_bot_token" > secrets/telegram_bot_token.txt
echo "your_api_key" > secrets/openai_api_key.txt
chmod 600 secrets/*.txt

# Запуск с секретами
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 🔧 Makefile команды

### Development

```bash
make dev-build      # Сборка образов
make dev-up         # Запуск
make dev-down       # Остановка
make dev-logs       # Логи
```

### Production

```bash
make prod-pull      # Pull образов
make prod-up        # Запуск
make prod-down      # Остановка
make prod-update    # Обновление
```

### Базовые операции

```bash
make up             # Запуск
make down           # Остановка
make restart        # Перезапуск
make status         # Статус
make logs           # Логи
make health         # Проверка здоровья
```

### База данных

```bash
make db-backup          # Backup
make db-restore FILE=   # Restore
make db-list-backups    # Список бэкапов
```

### Управление

```bash
make clean          # Очистка
make clean-all      # Полная очистка
make clean-logs     # Очистка логов
```

### Утилиты

```bash
make help           # Список всех команд
make config         # Показать конфигурацию
make env-example    # Создать .env из примера
make env-validate   # Проверить конфигурацию
make secrets-setup  # Настроить secrets
```

---

## 🔒 Безопасность

### Секреты

1. **Development**: Используйте `.env` файл
2. **Production**: Используйте Docker secrets в `secrets/`

### Рекомендации

- ✅ Не коммитьте `.env` и файлы секретов в git
- ✅ Используйте `chmod 600` для файлов секретов
- ✅ Настройте firewall (только необходимые порты)
- ✅ Используйте reverse proxy с SSL/TLS
- ✅ Регулярно обновляйте образы
- ✅ Настройте автоматическое резервное копирование

---

## 📊 Мониторинг

### Healthchecks

Все сервисы имеют встроенные healthchecks:

```bash
# Проверка через Docker
docker-compose ps

# Проверка через API
curl http://89.223.67.136:8004/health
curl http://89.223.67.136:3004
```

### Логи

```bash
# JSON формат с ротацией
# Максимум: 10MB на файл, 3 файла (dev), 50MB/10 файлов (prod)

# Просмотр
docker-compose logs -f [service]
```

### Метрики

```bash
# Использование ресурсов
docker stats

# Информация о volumes
docker volume ls
docker volume inspect telegram-bot-data
```

---

## 🆘 Troubleshooting

Смотрите [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#troubleshooting) для детального руководства по решению проблем.

### Быстрые решения

```bash
# Пересоздание контейнера
docker-compose up -d --force-recreate [service]

# Проверка конфигурации
docker-compose config

# Просмотр логов
docker-compose logs [service]

# Очистка и перезапуск
docker-compose down
docker system prune -f
docker-compose up -d
```

---

## 📖 Дополнительная документация

- [QUICKSTART.md](QUICKSTART.md) - Быстрый старт за 5 минут
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Полное руководство по развертыванию
- [secrets/README.md](secrets/README.md) - Управление секретами
- [Makefile](Makefile) - Все доступные команды

---

## 🎉 Заключение

Вы получили полную систему оркестрации с:

✅ Production-ready конфигурацией
✅ Development environment
✅ Healthchecks и мониторингом
✅ Resource limits
✅ Secrets management
✅ Logging с ротацией
✅ Резервным копированием
✅ Документацией

**Следующие шаги:**

1. Прочитайте [QUICKSTART.md](QUICKSTART.md)
2. Настройте `.env` файл
3. Запустите систему
4. Настройте мониторинг
5. Настройте автоматическое резервное копирование

---

**Версия**: 1.0.0
**Дата**: 2024
**Автор**: Telegram Bot Team
