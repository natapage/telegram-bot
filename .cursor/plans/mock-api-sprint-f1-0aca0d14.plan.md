<!-- 0aca0d14-6a6b-4df1-b3ad-43230cdc5d20 6cf24f30-51de-4355-b8b6-e7e547f7222f -->
# План Спринта F1: Mock API для дашборда статистики

## Цель

Создать Mock API с реалистичными тестовыми данными для независимой разработки frontend дашборда статистики диалогов

## Шаги реализации

### 1. Документ функциональных требований к дашборду

Создать `doc/dashboard-requirements.md`:

- Описание метрик общей статистики (total dialogs, active users, avg dialog length)
- Описание графика активности по времени (hourly data points)
- Описание списка последних диалогов (последние 10)
- Описание топа пользователей по активности (топ 5)
- Описание фильтрации по периодам (day/week/month)

### 2. Проектирование контракта API

Создать `src/api/schemas.py` с dataclasses:

- `OverallStats` - общая статистика (total_dialogs, active_users, avg_dialog_length)
- `ActivityDataPoint` - точка на графике (timestamp, message_count)
- `DialogPreview` - превью диалога (user_id, last_message, created_at, message_count)
- `UserActivity` - активность пользователя (user_id, message_count, last_active)
- `StatsResponse` - основной ответ API (overall, activity_data, recent_dialogs, top_users)

Создать `doc/api-contract-example.json` с примером JSON ответа

### 3. Интерфейс StatCollector

Создать `src/api/stat_collector.py`:

- `StatCollectorProtocol` (Protocol) с методом `async def get_stats(period: str) -> StatsResponse`
- Enum `StatsPeriod` с значениями DAY, WEEK, MONTH

### 4. Mock реализация

Создать `src/api/mock_stat_collector.py`:

- Класс `MockStatCollector` реализующий `StatCollectorProtocol`
- Метод `_generate_overall_stats(period)` - генерация общей статистики
- Метод `_generate_activity_data(period)` - генерация данных графика (24 точки для day, 7 для week, 30 для month)
- Метод `_generate_recent_dialogs()` - генерация 10 последних диалогов
- Метод `_generate_top_users()` - генерация топ 5 пользователей
- Реалистичные данные с использованием datetime для периодов

### 5. FastAPI endpoint

Создать `src/api/app.py`:

- FastAPI приложение с настройкой CORS
- GET `/stats` endpoint с query параметром `period: str = Query(..., enum=["day", "week", "month"])`
- Dependency injection для StatCollector
- Автоматическая документация OpenAPI (встроенная в FastAPI)
- GET `/health` endpoint для проверки работы API

### 6. Entrypoint для запуска API

Создать `src/api_main.py`:

- Инициализация MockStatCollector
- Запуск uvicorn на порту 8000
- Настройка логирования

### 7. Зависимости

Добавить в `pyproject.toml`:

- `fastapi>=0.115.0`
- `uvicorn[standard]>=0.32.0`

### 8. Команды Makefile

Обновить `Makefile`:

- `run-api` - запуск API сервера (`uv run python -m src.api_main`)
- `test-api` - тестирование endpoint через curl или PowerShell
- `api-docs` - открыть Swagger UI (`echo "Open http://localhost:8000/docs"`)

### 9. Документация и примеры

Создать `doc/api-examples.md` с примерами:

- curl запросы для Windows (Git Bash) и Linux/Mac
- PowerShell команды для Windows
- Примеры ответов для каждого периода

Обновить `frontend/README.md`:

- Добавить раздел "Mock API" с инструкциями по запуску
- Ссылка на doc/api-examples.md
- Ссылка на OpenAPI документацию

### 10. Финализация спринта

- Протестировать все endpoints
- Обновить `doc/frontend-roadmap.md`:
  - Изменить статус спринта F1 на "Завершено"
  - Добавить ссылку на этот план в колонку "План реализации"

## Файловая структура

```
src/
├── api/
│   ├── __init__.py
│   ├── app.py              # FastAPI приложение
│   ├── schemas.py          # Data contracts (dataclasses)
│   ├── stat_collector.py   # Protocol interface
│   └── mock_stat_collector.py  # Mock реализация
├── api_main.py             # Entrypoint для API
doc/
├── dashboard-requirements.md
├── api-contract-example.json
└── api-examples.md         # Примеры запросов
```

## Критерии приемки

- API запускается командой `make run-api`
- Endpoint GET /stats?period=day|week|month возвращает корректный JSON
- OpenAPI документация доступна на http://localhost:8000/docs
- Mock данные реалистичны и соответствуют периодам
- Все dataclasses имеют type hints
- Код проходит `make lint`
- Документация актуализирована (frontend-roadmap.md обновлен)

### To-dos

- [ ] Создать документ функциональных требований к дашборду
- [ ] Спроектировать контракт API (dataclasses и JSON пример)
- [ ] Создать интерфейс StatCollector (Protocol)
- [ ] Реализовать MockStatCollector с генерацией данных
- [ ] Создать FastAPI приложение с endpoint /stats
- [ ] Создать entrypoint для запуска API сервера
- [ ] Добавить FastAPI и uvicorn в зависимости
- [ ] Добавить команды run-api, test-api в Makefile
- [ ] Обновить документацию с инструкциями по Mock API