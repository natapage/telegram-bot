# Docker Quickstart

## Два способа запуска

Проект поддерживает два способа работы с Docker:

1. **Локальная сборка** - собирает образы из исходников на вашей машине
2. **Registry образы** - использует готовые образы из GitHub Container Registry

## Локальная сборка

### Когда использовать

- Разработка и отладка кода
- Тестирование изменений в Dockerfile
- Нет доступа к интернету или ghcr.io
- Первый запуск проекта

### Команды

```bash
# Создать .env файл
cp .env.example .env
# Отредактировать .env и добавить TELEGRAM_BOT_TOKEN, OPENAI_API_KEY

# Собрать и запустить все сервисы
make docker-up

# Или вручную
docker-compose up -d

# Пересобрать образы после изменений
make docker-build

# Просмотр логов
make docker-logs

# Статус сервисов
make docker-status

# Остановить сервисы
make docker-down

# Остановить и удалить volumes
make docker-clean
```

### Применение миграций

```bash
docker-compose exec api uv run alembic upgrade head
```

### Особенности

- **Сборка**: ~90-120 секунд при первом запуске
- **Файлы**: Использует `docker-compose.yml`
- **Изменения**: При изменении кода нужно пересобирать образ

## Registry образы (GitHub Container Registry)

### Когда использовать

- Production развертывание
- Тестирование стабильной версии
- Быстрый запуск без сборки
- CI/CD pipeline
- Развертывание на сервере

### Команды

```bash
# Создать .env файл (если еще нет)
cp .env.example .env
# Отредактировать .env и добавить TELEGRAM_BOT_TOKEN, OPENAI_API_KEY

# Pull последних образов из registry
make docker-pull

# Запустить сервисы с образами из registry
make docker-up-registry

# Или вручную
docker-compose -f docker-compose.registry.yml up -d

# Просмотр логов
make docker-logs-registry

# Статус сервисов
make docker-status-registry

# Остановить сервисы
make docker-down-registry
```

### Доступные образы

Образы публикуются автоматически при push в `main` ветку:

```
ghcr.io/natapage/telegram-bot-bot:latest
ghcr.io/natapage/telegram-bot-api:latest
ghcr.io/natapage/telegram-bot-frontend:latest
```

### Особенности

- **Сборка**: Не требуется, образы уже собраны
- **Скорость**: ~10-30 секунд для pull и запуска
- **Файлы**: Использует `docker-compose.registry.yml`
- **Обновления**: `make docker-pull` для получения свежих образов

### Применение миграций

```bash
docker-compose -f docker-compose.registry.yml exec api uv run alembic upgrade head
```

## Доступ к сервисам

После запуска (любым способом):

- **Frontend**: http://localhost:3001
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Сравнение

| Аспект | Локальная сборка | Registry образы |
|--------|------------------|-----------------|
| Скорость первого запуска | ~90-120 сек | ~10-30 сек |
| Требует сборки | Да | Нет |
| Подходит для разработки | ✅ Да | ❌ Нет |
| Подходит для production | ❌ Нет | ✅ Да |
| Требует интернет | Нет (после первой сборки) | Да (для pull) |
| Размер на диске | Больше (исходники + образы) | Меньше (только образы) |
| Обновления | `make docker-build` | `make docker-pull` |
| Изменения кода | Сразу видны после rebuild | Не видны (фиксированная версия) |

## Выбор образов для production

### Latest tag (рекомендуется для staging)

```yaml
image: ghcr.io/natapage/telegram-bot-api:latest
```

- Всегда последняя версия из `main`
- Автоматические обновления
- Может содержать незамеченные баги

### SHA tag (рекомендуется для production)

```yaml
image: ghcr.io/natapage/telegram-bot-api:sha-abc123f
```

- Фиксированная версия
- Воспроизводимость
- Стабильность

## Troubleshooting

### Ошибка: Cannot pull image

**Проблема**: Образы не могут быть загружены из registry

**Решение**:
1. Проверить интернет соединение
2. Убедиться что образы опубликованы: https://github.com/natapage?tab=packages
3. Проверить что образы публичные (public access)

### Ошибка: Port already in use

**Проблема**: Порты 3001 или 8000 уже заняты

**Решение**:
```bash
# Остановить локальную сборку если запущена
make docker-down

# Или остановить registry версию
make docker-down-registry

# Или изменить порты в docker-compose файле
```

### Образы устарели

**Проблема**: Запускается старая версия после обновления кода

**Решение**:

Для локальной сборки:
```bash
make docker-build
make docker-up
```

Для registry образов:
```bash
make docker-down-registry
make docker-pull
make docker-up-registry
```

## Best Practices

### Разработка

1. Используйте **локальную сборку** для активной разработки
2. Пересобирайте образы после изменений: `make docker-build`
3. Проверяйте логи: `make docker-logs`

### Тестирование

1. Используйте **registry образы** для тестирования интеграций
2. Pull свежих образов перед тестами: `make docker-pull`
3. Используйте фиксированные SHA теги для воспроизводимости

### Production

1. Используйте **registry образы** с SHA тегами
2. Не используйте `latest` для production
3. Тестируйте образы на staging перед production
4. Документируйте какой SHA используется в production

## Дополнительные команды

### Просмотр образов на машине

```bash
docker images | grep telegram-bot
```

### Удаление старых образов

```bash
docker image prune -a
```

### Проверка размера образов

```bash
docker images ghcr.io/natapage/telegram-bot-*
```

### Логи конкретного сервиса

```bash
# Локальная сборка
docker-compose logs -f bot
docker-compose logs -f api
docker-compose logs -f frontend

# Registry образы
docker-compose -f docker-compose.registry.yml logs -f bot
```

## Ресурсы

- **GitHub Actions**: `.github/workflows/build.yml`
- **Образы**: https://github.com/natapage?tab=packages
- **Документация**: `devops/doc/guides/github-actions-intro.md`
- **Настройка registry**: `devops/doc/guides/github-registry-setup.md`
