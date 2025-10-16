# Модель данных проекта

## Обзор

Проект использует SQLite для персистентного хранения истории диалогов пользователей с ботом.

## Технологический стек

- **База данных**: SQLite
- **Async драйвер**: aiosqlite
- **Миграции**: Alembic
- **Подход**: Raw SQL (без ORM)

## Схема базы данных

### Таблица `users`

Хранит информацию о пользователях Telegram.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY NOT NULL,              -- Telegram user ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_deleted BOOLEAN DEFAULT 0 NOT NULL          -- Soft delete flag
);
```

**Поля:**
- `id` - уникальный идентификатор пользователя Telegram (используется как PK)
- `created_at` - дата и время первого взаимодействия с ботом
- `is_deleted` - флаг мягкого удаления (0 = активен, 1 = удален)

### Таблица `messages`

Хранит историю сообщений пользователей и ответов бота.

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,                      -- FK to users.id
    role TEXT NOT NULL,                            -- 'user' or 'assistant'
    content TEXT NOT NULL,                         -- Текст сообщения
    length INTEGER NOT NULL,                       -- Длина в символах
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_deleted BOOLEAN DEFAULT 0 NOT NULL,         -- Soft delete flag
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_messages_user_deleted_created
    ON messages(user_id, is_deleted, created_at);
```

**Поля:**
- `id` - автоинкрементный уникальный идентификатор сообщения
- `user_id` - ссылка на пользователя (FK к `users.id`)
- `role` - роль отправителя:
  - `'user'` - сообщение от пользователя
  - `'assistant'` - ответ бота
  - `'system'` - системное сообщение (не хранится в БД, добавляется runtime)
- `content` - текст сообщения
- `length` - длина сообщения в символах (для аналитики)
- `created_at` - дата и время создания сообщения
- `is_deleted` - флаг мягкого удаления

**Индексы:**
- Композитный индекс `(user_id, is_deleted, created_at)` для эффективных запросов истории

## Стратегия Soft Delete

Проект использует стратегию **мягкого удаления** (soft delete):

- Данные физически не удаляются из базы данных
- При "удалении" устанавливается флаг `is_deleted = 1`
- Все запросы фильтруют данные по условию `is_deleted = 0`

### Преимущества:
- Возможность восстановления данных
- Аудит и аналитика
- Безопасность от случайного удаления
- Соблюдение возможных требований по хранению данных

### Команда `/clear`:
При выполнении команды `/clear`:
1. Все сообщения пользователя помечаются `is_deleted = 1`
2. История диалога становится недоступной
3. Данные остаются в БД для возможного восстановления

## Системный промпт

**Важно**: Системный промпт НЕ хранится в базе данных.

- Загружается из конфигурации при каждом запросе истории
- Добавляется в начало списка сообщений runtime
- Это упрощает схему БД и позволяет изменять промпт без миграций

## Репозиторий и операции

### MessageRepository

Класс `MessageRepository` предоставляет методы для работы с сообщениями:

```python
async def create_user(user_id: int) -> None
    """Создать пользователя (idempotent)"""

async def get_user_messages(user_id: int) -> list[dict]
    """Получить все не удаленные сообщения пользователя"""

async def add_message(user_id: int, role: str, content: str) -> None
    """Добавить новое сообщение (автоматически создает пользователя)"""

async def soft_delete_user_messages(user_id: int) -> None
    """Мягкое удаление всех сообщений пользователя"""
```

### Пример использования

```python
# Инициализация
config = Config()
database = Database(config)
repository = MessageRepository(database)

# Добавление сообщения
await repository.add_message(user_id=12345, role="user", content="Привет!")

# Получение истории
messages = await repository.get_user_messages(user_id=12345)
# Результат: [{"id": 1, "user_id": 12345, "role": "user", "content": "Привет!", "length": 7, ...}]

# Очистка истории (soft delete)
await repository.soft_delete_user_messages(user_id=12345)
```

## Миграции

### Управление миграциями

Миграции управляются через Alembic:

```bash
# Применить все миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Просмотреть текущее состояние
alembic current

# Создать новую миграцию
alembic revision -m "description"
```

### Структура миграций

```
alembic/
├── versions/
│   └── 3a933d9e6d4b_initial_schema.py  # Начальная схема
├── env.py                               # Конфигурация Alembic
└── script.py.mako                       # Шаблон миграций
```

### Первая миграция

Файл: `alembic/versions/3a933d9e6d4b_initial_schema.py`

Создает таблицы `users` и `messages` с индексами.

## Database Connection Manager

### Database класс

```python
class Database:
    """Менеджер подключений к базе данных"""

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[aiosqlite.Connection]:
        """Context manager для получения соединения"""
```

### Особенности:
- Async context manager для безопасной работы с соединениями
- Автоматический commit при успехе
- Автоматический rollback при ошибке
- Включены foreign keys (`PRAGMA foreign_keys = ON`)
- Row factory установлен в `aiosqlite.Row` для удобного доступа

### Пример использования:

```python
database = Database(config)

async with database.get_connection() as conn:
    await conn.execute("INSERT INTO users (id) VALUES (?)", (12345,))
    # Автоматический commit при выходе из контекста
```

## Конфигурация

### Переменная окружения

```env
# В .env файле
DATABASE_URL=sqlite+aiosqlite:///./telegram_bot.db
```

### Формат URL:
- Продакшн: `sqlite+aiosqlite:///./telegram_bot.db` (относительный путь)
- Тесты: `sqlite+aiosqlite:///file:test_db?mode=memory&cache=shared` (in-memory shared)

## Тестирование

### Test fixtures

```python
@pytest_asyncio.fixture
async def test_database(monkeypatch):
    """In-memory SQLite база для тестов"""
    test_db_url = "sqlite+aiosqlite:///file:test_db?mode=memory&cache=shared"
    monkeypatch.setenv("DATABASE_URL", test_db_url)
    # ... создание таблиц
```

### Особенности тестовой БД:
- Используется shared in-memory база
- Таблицы создаются в fixture
- Автоматическая очистка после каждого теста
- Быстрая работа тестов (все в памяти)

## Будущие расширения

### Возможные улучшения модели данных:

1. **Таблица `conversations`**
   - Группировка сообщений по сессиям/темам
   - Метаданные о разговоре

2. **Таблица `user_preferences`**
   - Настройки пользователя
   - Предпочитаемый язык
   - Персонализация

3. **Full-Text Search (FTS5)**
   - Поиск по истории сообщений
   - Виртуальная таблица для FTS

4. **Аналитические поля**
   - Время ответа бота
   - Использованная модель LLM
   - Токены запроса/ответа

5. **Audit log**
   - История изменений
   - Кто и когда изменил данные

## Производительность

### Текущие оптимизации:
- Композитный индекс для частых запросов
- Использование prepared statements через параметризованные запросы
- Async I/O для неблокирующих операций

### Рекомендации:
- Периодическая очистка старых soft-deleted записей
- Мониторинг размера базы данных
- VACUUM для оптимизации файла БД

## Безопасность

### Меры безопасности:
- Параметризованные запросы (защита от SQL injection)
- Foreign key constraints для целостности данных
- Валидация входных данных на уровне приложения
- База данных в `.gitignore` (не коммитится)

### Рекомендации:
- Регулярные бэкапы базы данных
- Ограничение прав доступа к файлу БД
- Шифрование БД для чувствительных данных (опционально)
