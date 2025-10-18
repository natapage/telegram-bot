# Чеклист проверки Спринта D0

Используйте этот чеклист для проверки работоспособности Docker setup.

## Предварительные проверки

### 1. Наличие файлов

Проверьте, что все файлы созданы:

```bash
# Корневая директория
ls Dockerfile.bot Dockerfile.api Dockerfile.frontend
ls docker-compose.yml .dockerignore .env.example

# Frontend директория
ls frontend/.dockerignore
```

Ожидаемый результат: все файлы существуют

### 2. Проверка документации

```bash
# Документация
ls devops/doc/plans/d0-docker-setup-plan.md
ls SPRINT_D0_SUMMARY.md
ls DOCKER_QUICKSTART.md
ls devops/doc/D0_IMPLEMENTATION_REPORT.md
```

## Настройка окружения

### 3. Создать .env файл

```bash
cp .env.example .env
```

### 4. Отредактировать .env

Открыть `.env` и заполнить:
- `TELEGRAM_BOT_TOKEN=<ваш_токен_от_BotFather>`
- `OPENAI_API_KEY=<ваш_ключ_от_Openrouter>`

Остальные значения можно оставить по умолчанию.

## Запуск и проверка

### 5. Сборка образов

```bash
make docker-build
```

Или напрямую:
```bash
docker-compose build
```

**Ожидаемый результат**:
- Успешная сборка всех 3 образов
- Нет ошибок в процессе сборки

### 6. Запуск сервисов

```bash
make docker-up
```

Или:
```bash
docker-compose up -d
```

**Ожидаемый результат**:
- Все 3 контейнера созданы и запущены
- Нет ошибок при запуске

### 7. Проверка статуса

```bash
make docker-status
```

Или:
```bash
docker-compose ps
```

**Ожидаемый результат**:
```
NAME                  STATUS
telegram-api          Up
telegram-bot          Up
telegram-frontend     Up
```

### 8. Применение миграций (если нужно)

```bash
docker-compose exec api uv run alembic upgrade head
```

**Ожидаемый результат**:
- Миграции применены успешно
- Или "Already at head" если уже применены

### 9. Проверка логов

```bash
make docker-logs
```

Или для каждого сервиса отдельно:
```bash
docker-compose logs api
docker-compose logs bot
docker-compose logs frontend
```

**Ожидаемый результат**:
- API: сообщение о запуске на порту 8000
- Bot: сообщение "Бот запущен..."
- Frontend: сообщение о запуске Next.js на порту 3000
- Нет критических ошибок

### 10. Проверка веб-сервисов

#### Frontend
Открыть в браузере: http://localhost:3000

**Ожидаемый результат**: страница загружается, показывается дашборд

#### API
Открыть в браузере: http://localhost:8000/docs

**Ожидаемый результат**: Swagger UI с документацией API

#### API Health Check
```bash
curl http://localhost:8000/health
```

**Ожидаемый результат**:
```json
{"status": "ok"}
```

### 11. Проверка Telegram бота

1. Открыть Telegram
2. Найти вашего бота (по токену)
3. Отправить `/start`

**Ожидаемый результат**:
- Бот отвечает приветственным сообщением
- Бот работает и может отвечать на сообщения

### 12. Проверка персистентности

```bash
# Остановить сервисы
make docker-down

# Запустить снова
make docker-up

# Проверить логи
make docker-logs
```

**Ожидаемый результат**:
- Сервисы запускаются без ошибок
- База данных сохранилась (файл telegram_bot.db)
- История диалогов доступна

## Проблемы и решения

### Проблема: Порт 8000 или 3000 занят

**Решение**: Изменить порты в `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # для api
  - "3001:3000"  # для frontend
```

### Проблема: Ошибка сборки образа

**Решение**:
1. Проверить наличие файлов `pyproject.toml`, `uv.lock`
2. Проверить наличие директорий `src/`, `prompts/`, `frontend/`
3. Очистить кеш Docker: `docker system prune -f`
4. Пересобрать: `make docker-build`

### Проблема: Bot не запускается

**Решение**:
1. Проверить токен в `.env`
2. Проверить логи: `docker-compose logs bot`
3. Убедиться, что промпт файл существует: `ls prompts/music_consultant.txt`

### Проблема: API не отвечает

**Решение**:
1. Проверить логи: `docker-compose logs api`
2. Убедиться, что база данных доступна: `ls telegram_bot.db`
3. Применить миграции: `docker-compose exec api uv run alembic upgrade head`

### Проблема: Frontend не загружается

**Решение**:
1. Проверить логи: `docker-compose logs frontend`
2. Убедиться, что API доступен: `curl http://localhost:8000/health`
3. Проверить переменную NEXT_PUBLIC_API_URL в `docker-compose.yml`

## Очистка и перезапуск

### Мягкая перезагрузка

```bash
make docker-down
make docker-up
```

### Полная перезагрузка с пересборкой

```bash
make docker-down
make docker-build
make docker-up
```

### Полная очистка (удалить всё)

```bash
make docker-clean
```

**Внимание**: Это удалит volumes (БД и логи)!

## Финальная проверка

- [ ] Все 3 сервиса запущены и работают
- [ ] Frontend доступен на http://localhost:3000
- [ ] API доступен на http://localhost:8000
- [ ] API Docs доступны на http://localhost:8000/docs
- [ ] Telegram бот отвечает на сообщения
- [ ] База данных персистентна (сохраняется после перезапуска)
- [ ] Логи доступны через `make docker-logs`

## Успех!

Если все пункты выполнены ✅, то **Спринт D0 завершен успешно!**

Проект готов к локальной разработке через Docker.

## Следующие шаги

- Ознакомиться с [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) для повседневной работы
- Прочитать [SPRINT_D0_SUMMARY.md](SPRINT_D0_SUMMARY.md) для деталей
- Подготовиться к Спринту D1: Build & Publish (GitHub Actions + GHCR)
