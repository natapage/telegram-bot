# Frontend - Telegram Bot Dashboard

> Web-интерфейс для управления и мониторинга Telegram бота с дашбордом статистики и ИИ-чатом

---

## 📋 Описание

Современный web-интерфейс на базе Next.js для взаимодействия с Telegram ботом, включающий:

- **Dashboard статистики** - визуализация метрик и аналитики по диалогам
- **ИИ-чат** - интерактивный веб-интерфейс для администратора (будущий спринт)

---

## 🎯 Статус проекта

**Текущий этап**: ✅ Спринт F3 - Dashboard UI реализован

См. [Frontend Roadmap](../doc/frontend-roadmap.md) для полного плана развития.

---

## 🛠️ Технологический стек

- **Framework**: Next.js 15 (App Router)
- **Язык**: TypeScript 5.x (strict mode)
- **UI Library**: shadcn/ui + Radix UI
- **Styling**: Tailwind CSS 4.x
- **Пакетный менеджер**: pnpm
- **Testing**: Vitest + React Testing Library
- **Linting**: ESLint + Prettier

**Почему этот стек?** См. [ADR документ](doc/adr-tech-stack.md)

---

## ⚙️ Требования к системе

- **Node.js** >= 18.0.0
- **pnpm** >= 9.0.0 (установка: `npm install -g pnpm`)
- **Backend API** запущен на http://localhost:8000 (для разработки)

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pnpm install
```

Или через Makefile из корня проекта:

```bash
make frontend-install
```

### 2. Настройка environment variables

Создайте `.env.local` файл (или используйте существующий):

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# GitHub Repository URL (замените на URL вашего репозитория)
NEXT_PUBLIC_GITHUB_REPO_URL=https://github.com/yourusername/telegram-bot
```

### 3. Запуск dev-сервера

```bash
pnpm dev
```

Или через Makefile:

```bash
make frontend-dev
```

Приложение будет доступно на: **http://localhost:3000**

### 4. Запуск Backend API (параллельно)

В отдельном терминале:

```bash
make run-api
```

API будет доступен на: **http://localhost:8000**

---

## 📁 Структура проекта

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page (Dashboard)
│   │   └── globals.css        # Global styles
│   ├── components/            # React компоненты
│   │   ├── ui/               # shadcn/ui компоненты
│   │   ├── dashboard/        # Dashboard компоненты ✨
│   │   │   ├── PeriodSelector.tsx     # Выбор периода
│   │   │   ├── OverallStats.tsx       # Карточки метрик
│   │   │   ├── ActivityChart.tsx      # График активности
│   │   │   ├── RecentDialogs.tsx      # Последние диалоги
│   │   │   └── TopUsers.tsx           # Топ пользователей
│   │   └── layout/           # Layout компоненты
│   ├── lib/                   # Утилиты и хелперы
│   │   ├── utils.ts          # shadcn utils
│   │   ├── api.ts            # API client
│   │   ├── types.ts          # TypeScript типы
│   │   └── format.ts         # Форматирование дат/чисел ✨
│   ├── hooks/                # Custom React hooks
│   │   └── useStats.ts       # Hook для загрузки статистики ✨
│   ├── config/               # Конфигурация
│   │   └── api.config.ts     # API endpoints
│   └── __tests__/            # Тесты ✨
│       └── setup.ts          # Vitest setup
├── doc/                       # Документация
│   ├── front-vision.md       # Техническое видение
│   ├── adr-tech-stack.md     # ADR для стека
│   └── plans/                # Планы спринтов
│       ├── s2-init-plan.md   # Sprint F2
│       └── s3-dashboard-plan.md  # Sprint F3 ✨
├── public/                    # Статические файлы
├── .env.local                 # Environment variables (не в git)
├── .env.example               # Пример переменных
├── package.json               # Dependencies и scripts
├── tsconfig.json              # TypeScript конфигурация
├── vitest.config.ts           # Vitest конфигурация
└── README.md                  # Этот файл
```

✨ - Добавлено в Sprint F3

---

## 🎨 Dashboard Компоненты

### PeriodSelector

Переключатель между периодами статистики (День/Неделя/Месяц).

**Props:**

```typescript
interface PeriodSelectorProps {
  period: Period;
  onPeriodChange: (period: Period) => void;
}
```

**Использование:**

```tsx
<PeriodSelector period={period} onPeriodChange={setPeriod} />
```

### OverallStats

Отображает 3 карточки с ключевыми метриками: всего диалогов, активных пользователей, средняя длина диалога.

**Props:**

```typescript
interface OverallStatsProps {
  stats: OverallStats;
}
```

### ActivityChart

График активности пользователей во времени (Recharts). Автоматически адаптирует ось X в зависимости от периода.

**Props:**

```typescript
interface ActivityChartProps {
  data: ActivityDataPoint[];
  period: Period;
}
```

### RecentDialogs

Таблица последних 10 диалогов с информацией о пользователях и сообщениях. Responsive design с адаптацией для mobile.

**Props:**

```typescript
interface RecentDialogsProps {
  dialogs: RecentDialog[];
}
```

### TopUsers

Список топ 5 самых активных пользователей с бейджами позиций.

**Props:**

```typescript
interface TopUsersProps {
  users: TopUser[];
}
```

### useStats Hook

Custom hook для загрузки статистики из API с управлением loading/error states.

**Возвращаемые значения:**

```typescript
interface UseStatsReturn {
  data: StatsResponse | null;
  loading: boolean;
  error: string | null;
  period: Period;
  setPeriod: (period: Period) => void;
  retry: () => void;
}
```

**Использование:**

```tsx
const { data, loading, error, period, setPeriod, retry } = useStats('day');
```

---

## 📜 Доступные команды

### Development

```bash
pnpm dev              # Запуск dev-сервера (http://localhost:3000)
pnpm build            # Production build
pnpm start            # Запуск production сервера
```

### Code Quality

```bash
pnpm lint             # Проверка кода ESLint
pnpm lint:fix         # Автофикс ESLint ошибок
pnpm format           # Форматирование кода Prettier
pnpm format:check     # Проверка форматирования
pnpm type-check       # TypeScript type checking
```

### Testing

```bash
pnpm test             # Запуск тестов (watch mode)
pnpm test:ui          # Запуск с UI интерфейсом
pnpm test:coverage    # Запуск с coverage отчетом
```

### Makefile команды (из корня проекта)

```bash
make frontend-install # Установка зависимостей
make frontend-dev     # Запуск dev-сервера
make frontend-build   # Production build
make frontend-lint    # Полная проверка (lint + format + types)
make frontend-test    # Запуск тестов
```

---

## 🔗 Интеграция с Backend

### Mock API (текущая разработка)

Backend предоставляет Mock API для независимой разработки frontend:

**Endpoints**:

- `GET /health` - health check
- `GET /stats?period={day|week|month}` - статистика по диалогам

**Документация API**:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- [API Examples](../doc/api-examples.md)
- [API Contract](../doc/api-contract-example.json)

### Real API (Sprint F5)

В будущем спринте F5 произойдет переключение с Mock на Real API с реальными данными из БД.
Для frontend это будет **прозрачно** - нужно будет только обновить env variable.

---

## 🧪 Тестирование

### Запуск тестов

```bash
pnpm test
```

### Структура тестов

```
src/
├── __tests__/
│   └── setup.ts                         # Глобальные настройки
├── hooks/__tests__/
│   └── useStats.test.ts                 # Тесты для useStats hook
└── components/dashboard/__tests__/
    ├── PeriodSelector.test.tsx          # Тесты для PeriodSelector
    ├── OverallStats.test.tsx            # Тесты для OverallStats
    ├── RecentDialogs.test.tsx           # Тесты для RecentDialogs
    └── TopUsers.test.tsx                # Тесты для TopUsers
```

### Coverage цели

- Critical components: >= 80%
- UI components: >= 70%
- Utils/helpers: >= 90%

---

## 🎨 Соглашения о кодировании

### TypeScript

- **Strict mode** - включен обязательно
- Никаких `any` - используем правильные типы
- Все функции и компоненты типизированы
- Предпочитаем `interface` для Props, `type` для unions

### React компоненты

```typescript
// Импорты
import { FC } from 'react';
import { ComponentProps } from './types';

// Типы
interface ComponentProps {
  title: string;
  onAction?: () => void;
}

// Компонент
export const Component: FC<ComponentProps> = ({ title, onAction }) => {
  // JSX
  return <div>{title}</div>;
};
```

### Styling

- **Tailwind CSS** для всех стилей
- **Mobile-first** approach
- Использовать semantic class names через `cn()` utility
- Следовать spacing scale: 4, 8, 12, 16, 24, 32px

### Форматирование

- Prettier настроен автоматически
- Запускать `pnpm format` перед commit
- Single quotes для строк
- Semicolons обязательны
- 100 символов line width

---

## 📚 Документация

### Проектная документация

- [Frontend Vision](doc/front-vision.md) - техническое видение
- [ADR Tech Stack](doc/adr-tech-stack.md) - обоснование выбора технологий
- [Sprint F2 Plan](doc/plans/s2-init-plan.md) - план инициализации
- [Frontend Roadmap](../doc/frontend-roadmap.md) - план развития

### Backend документация

- [Dashboard Requirements](../doc/dashboard-requirements.md) - требования к UI
- [Backend Vision](../docs/vision.md) - техническое видение backend

### Внешние ресурсы

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Vitest](https://vitest.dev/)

---

## 🗺️ Roadmap

| Спринт | Описание                         | Статус           |
| ------ | -------------------------------- | ---------------- |
| **F1** | Требования к дашборду и Mock API | ✅ Завершено     |
| **F2** | Инициализация Frontend проекта   | ✅ Завершено     |
| **F3** | Реализация Dashboard UI          | ✅ Завершено     |
| **F4** | Реализация ИИ-чата               | 🔵 Запланировано |
| **F5** | Переход с Mock на Real API       | 🔵 Запланировано |

Подробности: [Frontend Roadmap](../doc/frontend-roadmap.md)

---

## 🐛 Troubleshooting

### pnpm не найден

```bash
npm install -g pnpm
```

### API не отвечает

Убедитесь что Backend API запущен:

```bash
make run-api
```

Проверьте health check:

```bash
curl http://localhost:8000/health
```

### Ошибки TypeScript

```bash
pnpm type-check
```

Проверьте что все типы корректны в `tsconfig.json`

### Ошибки линтера

```bash
pnpm lint:fix
pnpm format
```

---

## 🤝 Contributing

1. Создайте feature branch
2. Следуйте соглашениям о кодировании
3. Запустите линтер и тесты
4. Убедитесь что type-check проходит
5. Создайте Pull Request

---

**Версия**: 0.3.0
**Дата обновления**: 2025-10-17
**Статус**: Sprint F3 завершен ✅

---

Made with ❤️ for Telegram Bot Dashboard
