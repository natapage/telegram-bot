# Secrets Management

Эта директория содержит файлы с чувствительными данными для production deployment.

## Структура

Создайте следующие файлы:

```bash
secrets/
├── telegram_bot_token.txt
└── openai_api_key.txt
```

## Использование

### Локальная разработка (development)

Для локальной разработки используйте `.env` файл:

```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваши ключи
```

### Production deployment

Для production используйте файлы секретов:

```bash
# Создайте файлы с секретами
echo "your_telegram_bot_token" > secrets/telegram_bot_token.txt
echo "your_openai_api_key" > secrets/openai_api_key.txt

# Установите правильные права доступа
chmod 600 secrets/*.txt

# Запустите с production конфигурацией
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Безопасность

1. **Никогда не коммитьте файлы с секретами в git**
2. Используйте `chmod 600` для файлов секретов
3. В production используйте внешние secret management системы:
   - AWS Secrets Manager
   - HashiCorp Vault
   - Kubernetes Secrets
   - Docker Secrets

## Docker Secrets

Секреты монтируются в контейнеры как read-only файлы в `/run/secrets/`:

```python
# Чтение секрета в приложении
with open('/run/secrets/telegram_bot_token', 'r') as f:
    token = f.read().strip()
```

## Ротация секретов

Для обновления секретов в production:

```bash
# 1. Обновите файл с секретом
echo "new_token" > secrets/telegram_bot_token.txt

# 2. Пересоздайте контейнеры
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --force-recreate
```

