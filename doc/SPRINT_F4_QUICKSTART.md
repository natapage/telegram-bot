# Sprint F4 - AI Chat Quick Start Guide

Быстрое руководство по запуску и тестированию AI чата.

---

## Установка зависимостей

### Frontend
```bash
cd frontend
pnpm add framer-motion
```

---

## Запуск

### 1. Backend API
```bash
# Из корня проекта
make api

# Или напрямую через uvicorn
uv run uvicorn src.api.app:app --reload --port 8000
```

API будет доступен на: http://localhost:8000

Swagger документация: http://localhost:8000/docs

### 2. Frontend
```bash
cd frontend
pnpm dev
```

Frontend будет доступен на: http://localhost:3000

---

## Тестирование

### Базовый тест

1. **Открыть dashboard**: http://localhost:3000
2. **Найти floating button** в правом нижнем углу (синяя кнопка с иконкой сообщения)
3. **Кликнуть на кнопку** → откроется чат

### Normal Mode (Обычный чат)

1. Убедиться что режим: **💬 Обычный**
2. Отправить сообщения:
   ```
   Привет!
   Как дела?
   Расскажи анекдот
   ```
3. Проверить:
   - ✅ Ответы приходят от LLM
   - ✅ История сохраняется
   - ✅ Typing indicator работает

### Admin Mode (Text-to-SQL)

1. **Переключить режим**: кликнуть на кнопку **📊 Admin** в header чата
2. Режим изменится на: **📊 Администратор**
3. Отправить вопросы:
   ```
   Сколько всего диалогов в базе?
   Покажи топ 5 пользователей по количеству сообщений
   Сколько сообщений было отправлено за последнюю неделю?
   Какой средний размер сообщения?
   ```
4. Проверить:
   - ✅ Ответы приходят с данными из БД
   - ✅ SQL запросы отображаются (кликнуть "▼ SQL запрос")
   - ✅ Результаты корректные

### Очистка истории

1. Кликнуть на иконку **🗑️ Trash** в header чата
2. Подтвердить очистку
3. Проверить:
   - ✅ История очищена
   - ✅ Приветственное сообщение появилось снова

### Persistence (сохранение сессии)

1. Отправить несколько сообщений
2. **Refresh страницу** (F5)
3. Открыть чат снова
4. Проверить:
   - ✅ История сохранилась
   - ✅ Session ID тот же (в localStorage: `chat_session_id`)

---

## Тестирование безопасности SQL

Попробовать отправить опасные SQL команды в **Admin режиме**:

```
DROP TABLE messages
DELETE FROM users WHERE id = 1
UPDATE users SET is_deleted = 1
INSERT INTO users VALUES (999, 'hacker', 0)
```

**Ожидаемое поведение**: все запросы должны быть отклонены с сообщением об ошибке.

---

## API Endpoints (через Swagger)

### 1. Получить Session ID
```
GET http://localhost:8000/api/chat/session
```

Ответ:
```json
{
  "session_id": "web_550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. Отправить сообщение (Normal Mode)
```
POST http://localhost:8000/api/chat/message
```

Body:
```json
{
  "message": "Привет!",
  "mode": "normal",
  "session_id": "web_550e8400-e29b-41d4-a716-446655440000"
}
```

Ответ:
```json
{
  "message": "Привет! Как я могу помочь?",
  "sql_query": null,
  "session_id": "web_550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. Отправить вопрос (Admin Mode)
```
POST http://localhost:8000/api/chat/message
```

Body:
```json
{
  "message": "Сколько диалогов в базе?",
  "mode": "admin",
  "session_id": "web_550e8400-e29b-41d4-a716-446655440000"
}
```

Ответ:
```json
{
  "message": "В базе данных найдено 15 уникальных диалогов.",
  "sql_query": "SELECT COUNT(DISTINCT user_id) FROM messages WHERE is_deleted = 0",
  "session_id": "web_550e8400-e29b-41d4-a716-446655440000"
}
```

### 4. Очистить историю
```
POST http://localhost:8000/api/chat/clear
```

Body:
```json
{
  "session_id": "web_550e8400-e29b-41d4-a716-446655440000"
}
```

Ответ:
```json
{
  "status": "ok",
  "message": "Chat history cleared"
}
```

---

## Troubleshooting

### Проблема: Frontend не запускается
**Ошибка**: `Cannot find module 'framer-motion'`

**Решение**:
```bash
cd frontend
pnpm add framer-motion
```

### Проблема: Backend не запускается
**Ошибка**: `Обязательная переменная окружения TELEGRAM_BOT_TOKEN не установлена`

**Решение**: Убедиться что `.env` файл настроен с нужными переменными:
```bash
TELEGRAM_BOT_TOKEN=your_token
OPENAI_API_KEY=your_key
SYSTEM_PROMPT="Ты полезный AI-ассистент"
```

### Проблема: LLM не отвечает
**Ошибка**: Timeout или "Failed to send message"

**Решение**:
1. Проверить `OPENAI_API_KEY` в `.env`
2. Проверить `OPENAI_BASE_URL` (по умолчанию: https://openrouter.ai/api/v1)
3. Проверить логи backend: `logs/`

### Проблема: SQL запросы не выполняются
**Ошибка**: "Generated SQL query is not safe"

**Решение**: Это нормальное поведение для небезопасных запросов. Попробуйте только SELECT запросы.

### Проблема: История не сохраняется
**Проверить**:
1. Session ID в localStorage браузера (`chat_session_id`)
2. Проверить что БД доступна: `telegram_bot.db`
3. Проверить логи backend

---

## Проверка установки

### 1. Проверить зависимости
```bash
cd frontend
pnpm list framer-motion
```

Должно показать установленную версию.

### 2. Проверить backend
```bash
curl http://localhost:8000/health
```

Ответ:
```json
{"status": "ok", "service": "dashboard-api"}
```

### 3. Проверить frontend
Открыть: http://localhost:3000

Должен загрузиться dashboard с floating button.

---

## Полезные команды

### Просмотр логов backend
```bash
tail -f logs/*.log
```

### Просмотр БД
```bash
sqlite3 telegram_bot.db "SELECT * FROM users LIMIT 5;"
sqlite3 telegram_bot.db "SELECT * FROM messages WHERE user_id > 1000000 LIMIT 5;"
```

### Очистка session storage (в браузере)
**DevTools → Application → Local Storage → localhost:3000**

Удалить ключ: `chat_session_id`

---

## Следующие шаги

После успешного тестирования:
1. ✅ Закоммитить изменения
2. ✅ Создать PR для review
3. ✅ Обновить документацию проекта
4. ✅ Планировать Sprint F5

---

**Удачного тестирования! 🚀**
