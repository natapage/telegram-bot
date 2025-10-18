# Руководство по развертыванию

Полное руководство по развертыванию Telegram Bot системы на сервере **89.223.67.136**.

## Содержание

1. [Быстрый старт](#быстрый-старт)
2. [Конфигурация](#конфигурация)
3. [Развертывание](#развертывание)
4. [Управление](#управление)
5. [Мониторинг](#мониторинг)
6. [Troubleshooting](#troubleshooting)

---

## Быстрый старт

### 1. Подготовка сервера

```bash
# SSH подключение к серверу
ssh root@89.223.67.136

# Установка Docker и Docker Compose (если не установлены)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
apt-get update
apt-get install docker-compose-plugin
```

### 2. Клонирование репозитория

```bash
# Создайте директорию для проекта
mkdir -p /opt/telegram-bot
cd /opt/telegram-bot

# Клонируйте репозиторий (или загрузите файлы)
git clone <your-repo-url> .
```

### 3. Настройка переменных окружения

```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env файл
nano .env
```

Обязательные параметры для заполнения:
```bash
TELEGRAM_BOT_TOKEN=your_actual_token_here
OPENAI_API_KEY=your_actual_api_key_here
API_PORT=8004
FRONTEND_PORT=3004
NEXT_PUBLIC_API_URL=http://89.223.67.136:8004
```

### 4. Настройка secrets (для production)

```bash
# Создайте файлы с секретами
mkdir -p secrets
echo "your_telegram_bot_token" > secrets/telegram_bot_token.txt
echo "your_openai_api_key" > secrets/openai_api_key.txt

# Установите правильные права доступа
chmod 600 secrets/*.txt
```

### 5. Запуск системы

#### Вариант A: Development (локальная сборка)

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

#### Вариант B: Production (образы из registry)

```bash
# Стандартный запуск
docker-compose up -d

# С production overrides
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 6. Проверка работы

```bash
# Проверка статуса контейнеров
docker-compose ps

# Проверка логов
docker-compose logs -f

# Проверка здоровья сервисов
curl http://localhost:8004/health
curl http://localhost:3004
```

---

## Конфигурация

### Порты

| Сервис   | Внутренний порт | Внешний порт | URL                           |
|----------|----------------|--------------|-------------------------------|
| API      | 8000           | 8004         | http://89.223.67.136:8004     |
| Frontend | 3000           | 3004         | http://89.223.67.136:3004     |
| Bot      | -              | -            | (внутренний сервис)           |

### Volumes

| Volume          | Назначение                | Backup |
|-----------------|---------------------------|--------|
| bot-data        | База данных SQLite (bot)  | ✅     |
| api-data        | База данных SQLite (api)  | ✅     |
| bot-logs        | Логи бота                 | ❌     |
| api-logs        | Логи API                  | ❌     |
| ./prompts       | Системные промпты         | ✅     |

### Network

- **Имя сети**: `telegram-network`
- **Драйвер**: bridge
- **Подсеть**: 172.28.0.0/16

---

## Развертывание

### Production Deployment

1. **Подготовка окружения**

```bash
# Создайте .env файл
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=your_token
OPENAI_API_KEY=your_key
API_PORT=8004
FRONTEND_PORT=3004
NEXT_PUBLIC_API_URL=http://89.223.67.136:8004
LOG_LEVEL=INFO
EOF
```

2. **Настройка secrets**

```bash
# Для production с docker secrets
mkdir -p secrets
echo "your_telegram_bot_token" > secrets/telegram_bot_token.txt
echo "your_openai_api_key" > secrets/openai_api_key.txt
chmod 600 secrets/*.txt
```

3. **Запуск с production конфигурацией**

```bash
# Pull последних образов
docker-compose pull

# Запуск с production overrides
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Проверка логов
docker-compose logs -f
```

4. **Настройка firewall**

```bash
# Открытие необходимых портов
ufw allow 8004/tcp
ufw allow 3004/tcp
ufw reload
```

### Обновление системы

```bash
# Pull новых образов
docker-compose pull

# Пересоздание контейнеров с новыми образами
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Удаление старых образов
docker image prune -f
```

### Rollback

```bash
# Откат к предыдущей версии
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

# Используйте конкретные версии образов в .env
BOT_VERSION=v1.0.0
API_VERSION=v1.0.0
FRONTEND_VERSION=v1.0.0

docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Управление

### Основные команды

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Перезапуск конкретного сервиса
docker-compose restart api

# Просмотр логов
docker-compose logs -f [service_name]

# Просмотр статуса
docker-compose ps

# Выполнение команды в контейнере
docker-compose exec api bash
```

### Управление данными

```bash
# Резервное копирование базы данных
docker cp telegram-api:/app/data/telegram_bot.db ./backups/telegram_bot_$(date +%Y%m%d).db

# Восстановление базы данных
docker cp ./backups/telegram_bot_20240101.db telegram-api:/app/data/telegram_bot.db
docker-compose restart api bot

# Очистка логов
docker-compose exec api sh -c "rm -rf /app/logs/*.log"
docker-compose exec bot sh -c "rm -rf /app/logs/*.log"
```

### Масштабирование

```bash
# Увеличение ресурсов для API
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale api=2
```

---

## Мониторинг

### Healthchecks

```bash
# Проверка здоровья API
curl http://localhost:8004/health

# Проверка здоровья Frontend
curl http://localhost:3004

# Статус всех healthchecks
docker-compose ps
```

### Логи

```bash
# Просмотр всех логов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f api
docker-compose logs -f bot
docker-compose logs -f frontend

# Последние 100 строк
docker-compose logs --tail=100 api

# Логи с временными метками
docker-compose logs -t api
```

### Метрики

```bash
# Использование ресурсов
docker stats

# Информация о контейнере
docker inspect telegram-api

# Использование дискового пространства
docker system df
```

---

## Troubleshooting

### Проблема: Контейнер не запускается

```bash
# Проверьте логи
docker-compose logs [service_name]

# Проверьте конфигурацию
docker-compose config

# Пересоздайте контейнер
docker-compose up -d --force-recreate [service_name]
```

### Проблема: База данных не доступна

```bash
# Проверьте volume
docker volume inspect telegram-api-data

# Проверьте права доступа
docker-compose exec api ls -la /app/data/

# Пересоздайте volume (ВНИМАНИЕ: потеря данных!)
docker-compose down -v
docker-compose up -d
```

### Проблема: API недоступен

```bash
# Проверьте, что контейнер запущен
docker-compose ps api

# Проверьте healthcheck
curl http://localhost:8004/health

# Проверьте порты
netstat -tulpn | grep 8004

# Проверьте firewall
ufw status
```

### Проблема: Frontend не может подключиться к API

```bash
# Проверьте переменную окружения
docker-compose exec frontend env | grep API_URL

# Обновите конфигурацию
# В .env установите:
NEXT_PUBLIC_API_URL=http://89.223.67.136:8004

# Пересоздайте frontend
docker-compose up -d --force-recreate frontend
```

### Проблема: Недостаточно ресурсов

```bash
# Проверьте использование ресурсов
docker stats

# Увеличьте лимиты в docker-compose.prod.yml
# Или освободите ресурсы:
docker system prune -a
docker volume prune
```

### Очистка системы

```bash
# Остановка всех контейнеров
docker-compose down

# Полная очистка (ВНИМАНИЕ: потеря всех данных!)
docker-compose down -v

# Удаление неиспользуемых образов
docker image prune -a

# Полная очистка Docker
docker system prune -a --volumes
```

---

## Резервное копирование

### Автоматическое резервное копирование

Создайте скрипт для автоматического бэкапа:

```bash
#!/bin/bash
# /opt/telegram-bot/backup.sh

BACKUP_DIR="/opt/backups/telegram-bot"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup базы данных
docker cp telegram-api:/app/data/telegram_bot.db $BACKUP_DIR/telegram_bot_$DATE.db

# Backup конфигурации
cp /opt/telegram-bot/.env $BACKUP_DIR/.env_$DATE
cp -r /opt/telegram-bot/prompts $BACKUP_DIR/prompts_$DATE

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -name "telegram_bot_*.db" -mtime +30 -delete

echo "Backup completed: $DATE"
```

Добавьте в cron:

```bash
# Ежедневный бэкап в 3:00
crontab -e
0 3 * * * /opt/telegram-bot/backup.sh >> /var/log/telegram-bot-backup.log 2>&1
```

---

## Безопасность

### Рекомендации

1. **Используйте secrets для production**
   ```bash
   # Не храните токены в .env на production
   # Используйте docker secrets или внешние secret managers
   ```

2. **Ограничьте доступ к портам**
   ```bash
   # Используйте reverse proxy (nginx) вместо прямого доступа
   # Настройте SSL/TLS
   ```

3. **Регулярно обновляйте образы**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

4. **Мониторьте логи**
   ```bash
   # Настройте централизованное логирование
   # Используйте системы мониторинга (Prometheus, Grafana)
   ```

---

## Дополнительные ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Project README](README.md)
- [Development Guide](docs/guides/06_development_workflow.md)
