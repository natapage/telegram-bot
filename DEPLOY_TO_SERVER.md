# 🚀 Развертывание на сервере 89.223.67.136

## Шаг 1: Подключение к серверу

```bash
ssh natalia@89.223.67.136
```

## Шаг 2: Установка Docker (если не установлен)

```bash
# Обновление системы
apt-get update
apt-get upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
apt-get install docker-compose-plugin -y

# Проверка установки
docker --version
docker compose version
```

## Шаг 3: Подготовка директории проекта

```bash
# Создание директории
mkdir -p ~/telegram-bot
cd ~/telegram-bot

# Клонирование репозитория (или загрузка файлов)
# Вариант 1: Если есть git репозиторий
git clone <your-repo-url> .

# Вариант 2: Загрузка файлов с локальной машины
# На локальной машине (Windows):
# scp -r C:\Users\Natalia\Desktop\AI\telegram-bot\* natalia@89.223.67.136:~/telegram-bot/
```

## Шаг 4: Настройка .env файла

```bash
cd ~/telegram-bot

# Создание .env из примера
cp ENV_EXAMPLE.txt .env

# Редактирование .env
nano .env
```

### Заполните обязательные параметры:

```bash
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=ваш_реальный_токен_от_BotFather

# OpenAI API Key
OPENAI_API_KEY=ваш_реальный_api_ключ

# Порты (уже настроены)
API_PORT=8004
FRONTEND_PORT=3004

# URL API (уже настроен)
NEXT_PUBLIC_API_URL=http://89.223.67.136:8004

# Остальное оставьте как есть
```

Сохраните файл: `Ctrl+O`, `Enter`, `Ctrl+X`

## Шаг 5: Настройка Firewall

```bash
# Открытие портов
ufw allow 22/tcp     # SSH
ufw allow 8004/tcp   # API
ufw allow 3004/tcp   # Frontend
ufw enable
ufw status
```

## Шаг 6: Запуск системы

### Вариант A: С локальной сборкой

```bash
cd /opt/telegram-bot

# Сборка образов
docker compose -f docker-compose.local.yml build

# Запуск
docker compose -f docker-compose.local.yml up -d

# Проверка логов
docker compose logs -f
```

### Вариант B: С registry образами (когда они будут доступны)

```bash
cd /opt/telegram-bot

# Pull образов
docker compose pull

# Запуск
docker compose up -d

# Проверка
docker compose ps
```

### Вариант C: С Makefile

```bash
cd /opt/telegram-bot

# Проверка доступности Makefile
make help

# Локальная сборка
make dev-build
make dev-up

# Production (когда образы доступны)
make prod-pull
make prod-up
```

## Шаг 7: Проверка работы

```bash
# Статус контейнеров
docker compose ps

# Проверка API
curl http://localhost:8004/health
curl http://89.223.67.136:8004/health

# Проверка Frontend
curl http://localhost:3004
curl http://89.223.67.136:3004

# Просмотр логов
docker compose logs -f api
docker compose logs -f bot
docker compose logs -f frontend
```

## Шаг 8: Настройка автозапуска (опционально)

```bash
# Создание systemd service
cat > /etc/systemd/system/telegram-bot.service << 'EOF'
[Unit]
Description=Telegram Bot Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/telegram-bot
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Включение и запуск
systemctl daemon-reload
systemctl enable telegram-bot.service
systemctl start telegram-bot.service
systemctl status telegram-bot.service
```

## Доступ к сервисам

После успешного запуска:

- **API**: http://89.223.67.136:8004
- **API Docs**: http://89.223.67.136:8004/docs
- **API Health**: http://89.223.67.136:8004/health
- **Frontend**: http://89.223.67.136:3004
- **Bot**: Telegram

## Управление системой

```bash
# Просмотр статуса
docker compose ps

# Просмотр логов
docker compose logs -f

# Перезапуск
docker compose restart

# Остановка
docker compose down

# Обновление
docker compose pull
docker compose up -d --force-recreate

# Backup базы данных
docker cp telegram-api:/app/data/telegram_bot.db ./backups/telegram_bot_$(date +%Y%m%d).db
```

## Troubleshooting

### Проблема: Порты заняты

```bash
# Проверка занятых портов
netstat -tulpn | grep 8004
netstat -tulpn | grep 3004

# Остановка процессов на портах
kill $(lsof -t -i:8004)
kill $(lsof -t -i:3004)
```

### Проблема: Контейнеры не запускаются

```bash
# Просмотр логов
docker compose logs

# Проверка ресурсов
df -h
free -h

# Очистка
docker system prune -a
```

### Проблема: Недостаточно прав

```bash
# Добавление пользователя в группу docker
usermod -aG docker $USER
newgrp docker
```

## Резервное копирование

```bash
# Создание директории для бэкапов
mkdir -p /opt/backups/telegram-bot

# Создание скрипта бэкапа
cat > /opt/telegram-bot/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/telegram-bot"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
docker cp telegram-api:/app/data/telegram_bot.db $BACKUP_DIR/telegram_bot_$DATE.db
cp /opt/telegram-bot/.env $BACKUP_DIR/.env_$DATE
find $BACKUP_DIR -name "telegram_bot_*.db" -mtime +30 -delete
echo "Backup completed: $DATE"
EOF

chmod +x /opt/telegram-bot/backup.sh

# Добавление в cron (ежедневно в 3:00)
(crontab -l 2>/dev/null; echo "0 3 * * * /opt/telegram-bot/backup.sh >> /var/log/telegram-bot-backup.log 2>&1") | crontab -
```

## Мониторинг

```bash
# Использование ресурсов
docker stats

# Логи в реальном времени
docker compose logs -f

# Проверка здоровья
watch -n 5 'docker compose ps'
```

---

## ✅ Чеклист готовности

- [ ] Docker и Docker Compose установлены
- [ ] Файлы проекта загружены в `/opt/telegram-bot`
- [ ] `.env` файл создан и заполнен
- [ ] Firewall настроен (порты 8004, 3004)
- [ ] Система запущена
- [ ] API отвечает на http://89.223.67.136:8004/health
- [ ] Frontend доступен на http://89.223.67.136:3004
- [ ] Бот отвечает в Telegram
- [ ] Настроено резервное копирование

---

**Готово!** 🎉 Ваша система развернута на сервере 89.223.67.136
