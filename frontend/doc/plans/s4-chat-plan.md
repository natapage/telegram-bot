# Sprint 4: Реализация ИИ-чата

## Цель

Создать веб-интерфейс для чата с AI-ассистентом, интегрированный в dashboard через floating button. Реализовать два режима работы: обычный чат с LLM и режим администратора с text-to-SQL для запросов к статистике.

## Архитектура

### Frontend компоненты

- `FloatingChatButton.tsx` - кнопка в правом нижнем углу
- `AIChatCard.tsx` - модальный чат (на базе референса 21st-ai-chat)
- `ChatModeToggle.tsx` - переключатель режимов (normal/admin)

### Backend endpoints

- `POST /api/chat/message` - отправка сообщения и получение ответа
- `POST /api/chat/clear` - очистка истории чата
- `GET /api/chat/session` - получение/создание session ID для веб-пользователя

### Режимы работы

1. **Normal mode**: стандартный чат с LLM (как в Telegram боте)
2. **Admin mode**: text-to-SQL pipeline для запросов к статистике

---

## Этапы реализации

### 1. Frontend: Базовый UI чата

**Файлы:**

- `frontend/src/components/ui/ai-chat.tsx` - компонент чата из референса
- `frontend/src/components/dashboard/FloatingChatButton.tsx` - floating button
- `frontend/src/components/dashboard/ChatContainer.tsx` - контейнер с popover логикой

**Задачи:**

1. Установить `framer-motion`: `pnpm add framer-motion`
2. Создать `ai-chat.tsx` на основе `doc/references/21st-ai-chat.md` (строки 76-201)
3. Адаптировать для проекта:

   - Перевести тексты на русский
   - Добавить props для режима (normal/admin)
   - Добавить индикатор текущего режима в header
   - Добавить toggle для переключения режимов

4. Создать `FloatingChatButton.tsx`:

   - Кнопка с иконкой MessageCircle (lucide-react)
   - Позиция: `fixed bottom-6 right-6`
   - При клике открывает `AIChatCard` в popover/modal

5. Интегрировать в `frontend/src/app/page.tsx` (после строки 139)

### 2. Frontend: API интеграция

**Файлы:**

- `frontend/src/lib/api.ts` - расширить API client
- `frontend/src/lib/types.ts` - добавить типы для чата
- `frontend/src/hooks/useChat.ts` - новый hook для чата

**Типы (`types.ts`):**

```typescript
export type ChatMode = 'normal' | 'admin';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  sql_query?: string; // для admin режима
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  mode: ChatMode;
  session_id: string;
}

export interface ChatResponse {
  message: string;
  sql_query?: string;
  session_id: string;
}
```

**API методы (`api.ts`):**

```typescript
async sendChatMessage(request: ChatRequest): Promise<ChatResponse>
async clearChat(sessionId: string): Promise<void>
async getOrCreateSession(): Promise<{ session_id: string }>
```

**Hook (`useChat.ts`):**

- State: messages, loading, error, mode, sessionId
- Functions: sendMessage, clearChat, toggleMode
- LocalStorage для сохранения sessionId

### 3. Backend: Chat API endpoints

**Файлы:**

- `src/api/app.py` - добавить chat endpoints
- `src/api/schemas.py` - добавить chat schemas
- `src/api/chat_service.py` - новый сервис для обработки чата

**Schemas (`schemas.py`):**

```python
@dataclass
class ChatRequest:
    message: str
    mode: str  # "normal" | "admin"
    session_id: str

@dataclass
class ChatResponse:
    message: str
    sql_query: str | None
    session_id: str
```

**Endpoints в `app.py`:**

1. `POST /api/chat/message` - принимает ChatRequest, возвращает ChatResponse
2. `POST /api/chat/clear` - очищает историю по session_id
3. `GET /api/chat/session` - генерирует новый session_id (UUID)

### 4. Backend: Session management для веб-пользователей

**Подход:**

- Веб-пользователи получают session_id в формате: `web_<uuid>`
- Хранятся в той же таблице `users` с ID = hash(session_id)
- `message_repository.py` уже поддерживает произвольные user_id

**Файлы:**

- `src/api/session_manager.py` - новый модуль для управления сессиями

**Функции:**

```python
def generate_session_id() -> str
def session_id_to_user_id(session_id: str) -> int  # hash для DB
```

### 5. Backend: Normal mode - обычный чат

**Файл:** `src/api/chat_service.py`

**Логика:**

1. Получить session_id из request
2. Конвертировать в user_id для БД
3. Использовать существующий `DialogManager` и `LLMClient`
4. Добавить сообщение пользователя в историю
5. Получить ответ от LLM
6. Сохранить ответ в историю
7. Вернуть ChatResponse

**Переиспользование:**

- `src/dialog_manager.py` - как есть
- `src/llm_client.py` - как есть
- `src/message_repository.py` - как есть

### 6. Backend: Admin mode - text-to-SQL

**Файл:** `src/api/text_to_sql_service.py`

**Pipeline:**

1. **Вопрос пользователя** → "Сколько диалогов за неделю?"
2. **Text-to-SQL промпт** → отправить в LLM с описанием схемы БД
3. **SQL генерация** → получить SQL запрос от LLM
4. **Выполнение SQL** → выполнить через Database
5. **Результат в текст** → отправить результаты в LLM для форматирования
6. **Ответ пользователю** → вернуть понятный текст

**Промпт для text-to-SQL:**

```
You are a SQL expert. Generate SQL query for SQLite database.

Schema:
- users (id, created_at, is_deleted)
- messages (id, user_id, role, content, length, created_at, is_deleted)

User question: {user_question}

Return only SQL query, no explanations.
```

**Безопасность:**

- Whitelist SQL операций: только SELECT
- Запрет DROP, DELETE, UPDATE, INSERT
- Timeout для запросов

### 7. Frontend: Доработка UX

**Улучшения:**

1. Auto-scroll к последнему сообщению
2. Отображение SQL запросов в admin режиме (collapsible block)
3. Кнопка "Очистить чат"
4. Индикатор режима в header чата
5. Persistence session_id в localStorage
6. Error boundaries для обработки ошибок

**Файлы:**

- `frontend/src/components/ui/ai-chat.tsx` - доработать компонент
- `frontend/src/components/dashboard/SqlQueryDisplay.tsx` - отображение SQL

### 8. Integration и тестирование

**Frontend:**

1. Проверить работу чата в normal режиме
2. Проверить переключение между режимами
3. Проверить persistence истории
4. Проверить responsive design
5. Проверить error handling

**Backend:**

1. Тестировать endpoints через `/docs`
2. Проверить session management
3. Проверить text-to-SQL с разными вопросами
4. Проверить безопасность SQL (попытки инъекций)
5. Проверить concurrent sessions

**Integration:**

1. End-to-end тест: открыть чат → отправить сообщение → получить ответ
2. Проверить работу с реальными данными из БД
3. Проверить admin mode с запросами к статистике

---

## Приоритизация

### Must have (MVP)

- ✅ Floating button и базовый UI чата
- ✅ Normal mode с интеграцией LLM
- ✅ Session management для веб-пользователей
- ✅ API endpoints для чата

### Should have

- ✅ Admin mode с text-to-SQL
- ✅ Отображение SQL запросов
- ✅ Переключатель режимов
- ✅ Persistence истории

### Nice to have (опционально)

- ⏳ Streaming ответов (Server-Sent Events)
- ⏳ Markdown рендеринг в сообщениях
- ⏳ Code syntax highlighting
- ⏳ Export истории чата

---

## Технические детали

### Session ID формат

- Frontend генерирует: `web_${crypto.randomUUID()}`
- Backend конвертирует в user_id: `hash(session_id) % 2147483647`

### Database schema

Переиспользуем существующие таблицы `users` и `messages`. Веб-пользователи хранятся с синтетическими ID.

### Text-to-SQL безопасность

```python
def is_safe_query(sql: str) -> bool:
    forbidden = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
    return not any(word in sql.upper() for word in forbidden)
```

---

## Файлы для создания/изменения

### Frontend (создать)

- `frontend/src/components/ui/ai-chat.tsx`
- `frontend/src/components/dashboard/FloatingChatButton.tsx`
- `frontend/src/components/dashboard/ChatContainer.tsx`
- `frontend/src/hooks/useChat.ts`

### Frontend (изменить)

- `frontend/src/lib/api.ts` - добавить chat методы
- `frontend/src/lib/types.ts` - добавить chat типы
- `frontend/src/app/page.tsx` - интегрировать FloatingChatButton

### Backend (создать)

- `src/api/chat_service.py`
- `src/api/text_to_sql_service.py`
- `src/api/session_manager.py`

### Backend (изменить)

- `src/api/app.py` - добавить chat endpoints
- `src/api/schemas.py` - добавить chat schemas

---

## Связанные документы

- `doc/references/21st-ai-chat.md` - референс UI компонента
- `frontend/doc/front-vision.md` - техническое видение
- `src/handler.py` - референс логики Telegram бота
- `src/llm_client.py` - клиент для LLM (переиспользуем)

---

**Версия**: 1.0
**Дата создания**: 2025-10-17
**Статус**: В работе
