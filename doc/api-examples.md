# Примеры запросов к API дашборда

> **Назначение**: Примеры использования Mock API для тестирования и разработки frontend
> **API URL**: http://localhost:8000
> **Документация**: http://localhost:8000/docs

---

## Запуск API

```bash
# Запустить API сервер
make run-api

# API будет доступен на http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## Health Check

### curl (Linux/Mac/Git Bash)

```bash
curl http://localhost:8000/health
```

### PowerShell (Windows)

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" | Select-Object -ExpandProperty Content
```

### Ответ

```json
{
  "status": "ok",
  "service": "dashboard-api"
}
```

---

## Получение статистики

### Статистика за день (day)

#### curl

```bash
curl "http://localhost:8000/stats?period=day"
```

#### PowerShell

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/stats?period=day" | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

#### Ответ (пример)

```json
{
  "overall": {
    "total_dialogs": 52,
    "active_users": 41,
    "avg_dialog_length": 11.5
  },
  "activity_data": [
    {
      "timestamp": "2025-10-17T00:00:00Z",
      "message_count": 15
    },
    {
      "timestamp": "2025-10-17T01:00:00Z",
      "message_count": 12
    }
    // ... еще 22 точки (24 часа)
  ],
  "recent_dialogs": [
    {
      "user_id": 123456789,
      "last_message": "Спасибо за помощь!",
      "created_at": "2025-10-17T18:45:23Z",
      "message_count": 15
    }
    // ... еще 9 диалогов
  ],
  "top_users": [
    {
      "user_id": 987654321,
      "message_count": 95,
      "last_active": "2025-10-17T19:30:00Z"
    }
    // ... еще 4 пользователя
  ],
  "period": "day"
}
```

---

### Статистика за неделю (week)

#### curl

```bash
curl "http://localhost:8000/stats?period=week"
```

#### PowerShell

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/stats?period=week" | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

#### Особенности данных

- `activity_data`: 7 точек (по дням недели)
- `overall.total_dialogs`: больше чем за день (~200-300)
- `overall.avg_dialog_length`: увеличивается (~10-18)

---

### Статистика за месяц (month)

#### curl

```bash
curl "http://localhost:8000/stats?period=month"
```

#### PowerShell

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/stats?period=month" | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

#### Особенности данных

- `activity_data`: 30 точек (по дням месяца)
- `overall.total_dialogs`: значительно больше (~800-1200)
- `overall.avg_dialog_length`: максимальное значение (~12-20)

---

## Тестирование через Makefile

```bash
# Запустить API
make run-api

# В другом терминале протестировать все endpoints
make test-api
```

Команда `make test-api` выполнит запросы к:
- GET /health
- GET /stats?period=day
- GET /stats?period=week
- GET /stats?period=month

И выведет отформатированные JSON ответы.

---

## Обработка ошибок

### Неверный период

#### Запрос

```bash
curl "http://localhost:8000/stats?period=invalid"
```

#### Ответ

```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["query", "period"],
      "msg": "Input should be 'day', 'week' or 'month'",
      "input": "invalid"
    }
  ]
}
```

HTTP статус: **422 Unprocessable Entity**

---

## Использование в JavaScript/TypeScript

### Fetch API

```javascript
// Получение статистики за день
const response = await fetch('http://localhost:8000/stats?period=day');
const data = await response.json();

console.log('Total dialogs:', data.overall.total_dialogs);
console.log('Active users:', data.overall.active_users);
console.log('Activity data points:', data.activity_data.length);
```

### Axios

```javascript
import axios from 'axios';

const getStats = async (period) => {
  const response = await axios.get('http://localhost:8000/stats', {
    params: { period }
  });
  return response.data;
};

// Использование
const dayStats = await getStats('day');
const weekStats = await getStats('week');
const monthStats = await getStats('month');
```

---

## Структура данных

Полный контракт API доступен в файле [api-contract-example.json](./api-contract-example.json)

### TypeScript типы (для frontend)

```typescript
interface OverallStats {
  total_dialogs: number;
  active_users: number;
  avg_dialog_length: number;
}

interface ActivityDataPoint {
  timestamp: string; // ISO 8601
  message_count: number;
}

interface DialogPreview {
  user_id: number;
  last_message: string;
  created_at: string; // ISO 8601
  message_count: number;
}

interface UserActivity {
  user_id: number;
  message_count: number;
  last_active: string; // ISO 8601
}

interface StatsResponse {
  overall: OverallStats;
  activity_data: ActivityDataPoint[];
  recent_dialogs: DialogPreview[];
  top_users: UserActivity[];
  period: 'day' | 'week' | 'month';
}
```

---

## Автоматическая документация

API предоставляет автоматически генерируемую документацию:

### Swagger UI (интерактивная)

**URL**: http://localhost:8000/docs

Позволяет:
- Просмотреть все endpoints
- Протестировать запросы прямо в браузере
- Увидеть схемы данных
- Скачать OpenAPI спецификацию

### ReDoc (документация)

**URL**: http://localhost:8000/redoc

Красивая документация в формате ReDoc:
- Удобная навигация
- Детальное описание параметров
- Примеры запросов и ответов

---

## Особенности Mock данных

1. **Детерминированность**: Данные генерируются с фиксированным seed (42), поэтому при одинаковых запросах получается одинаковый результат
2. **Реалистичность**:
   - График активности учитывает время суток (ночью меньше, вечером больше)
   - Неделя учитывает выходные (меньше активности)
   - Количество данных масштабируется с периодом
3. **Разнообразие**: Текстовые сообщения выбираются случайно из набора реалистичных фраз
4. **Консистентность**: Структура данных полностью соответствует контракту API

---

## Следующие шаги

После ознакомления с Mock API:

1. Изучите [функциональные требования к дашборду](./dashboard-requirements.md)
2. Начните разработку frontend компонентов
3. Интегрируйте frontend с Mock API
4. После завершения frontend переключитесь на Real API (Sprint F5)

---

**Версия**: 1.0
**Дата**: 2025-10-17
