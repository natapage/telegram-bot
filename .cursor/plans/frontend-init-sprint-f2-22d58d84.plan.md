<!-- 22d58d84-8f13-448f-ad5b-4167761ad149 c3f6b16a-5110-4984-b2da-75c87256a5f1 -->
# Sprint F2: Инициализация Frontend проекта

## Обзор

Создание технической основы frontend приложения с использованием Next.js, TypeScript, shadcn/ui и Tailwind CSS. Настройка инфраструктуры разработки, инструментов качества кода и интеграции с Mock API.

## Технологический стек

- **Framework**: Next.js 15 (App Router)
- **Язык**: TypeScript 5.x
- **UI Library**: shadcn/ui
- **Styling**: Tailwind CSS 3.x
- **Пакетный менеджер**: pnpm
- **Testing**: Vitest + React Testing Library
- **Linting**: ESLint + Prettier
- **Type Checking**: TypeScript strict mode

## Структура работ

### 1. Создание документации проекта

**Файл 1**: `frontend/doc/front-vision.md`

Создать архитектурное видение frontend проекта по аналогии с `docs/vision.md`:

- Цели и назначение frontend приложения
- Архитектурные принципы (компонентная структура, state management)
- Организация кода (App Router structure, компоненты, hooks, utils)
- Интеграция с API (Mock → Real переход)
- Соглашения о стилях и UI/UX
- План тестирования frontend компонентов

**Файл 2**: `frontend/doc/adr-tech-stack.md`

Создать Architecture Decision Record с обоснованием выбора технологий:

- Почему Next.js 15 (App Router) вместо Pages Router/других фреймворков
- Почему TypeScript strict mode
- Почему shadcn/ui вместо Material-UI/Ant Design/других UI библиотек
- Почему Tailwind CSS для стилизации
- Почему pnpm вместо npm/yarn
- Почему Vitest вместо Jest
- Критерии выбора и альтернативы
- Trade-offs и ограничения выбранного стека

### 2. Инициализация Next.js проекта

**Команда**: `pnpm create next-app@latest`

Параметры инициализации:

- TypeScript: Yes
- ESLint: Yes
- Tailwind CSS: Yes
- `src/` directory: Yes
- App Router: Yes
- Import alias (@/*): Yes

**Расположение**: `frontend/` директория

### 3. Настройка shadcn/ui

**Действия**:

1. Инициализировать shadcn/ui: `pnpm dlx shadcn@latest init`
2. Установить базовые компоненты для Dashboard:

   - `card` - для карточек метрик
   - `button` - для кнопок и элементов управления
   - `select` - для выбора периода (day/week/month)
   - `table` - для списка диалогов и топ пользователей
   - `chart` (если доступно) или использовать recharts

**Конфигурация**:

- Style: Default
- Base color: Slate
- CSS variables: Yes

### 4. Структура проекта

Организация директорий в `frontend/src/`:

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page (Dashboard)
│   └── globals.css        # Global styles
├── components/            # React компоненты
│   ├── ui/               # shadcn/ui компоненты (auto-generated)
│   ├── dashboard/        # Dashboard специфичные компоненты
│   │   ├── OverallStats.tsx
│   │   ├── ActivityChart.tsx
│   │   ├── RecentDialogs.tsx
│   │   ├── TopUsers.tsx
│   │   └── PeriodSelector.tsx
│   └── layout/           # Layout компоненты
│       ├── Header.tsx
│       └── Sidebar.tsx (опционально)
├── lib/                   # Утилиты и хелперы
│   ├── utils.ts          # shadcn/ui utils
│   ├── api.ts            # API client для Mock API
│   └── types.ts          # TypeScript типы/интерфейсы
├── hooks/                # Custom React hooks
│   └── useStats.ts       # Hook для получения статистики
└── config/               # Конфигурация
    └── api.config.ts     # API endpoints и настройки
```

### 5. Настройка инструментов разработки

**ESLint**:

- Расширить конфигурацию Next.js правилами
- Добавить правила для TypeScript strict mode
- Добавить правила для React hooks

**Prettier**:

- Создать `.prettierrc`
- Интеграция с ESLint
- Настройка форматирования под проект

**TypeScript**:

- Strict mode enabled
- Path aliases настроены (@/*)
- Типизация для API responses

**Vitest**:

- Установить `vitest`, `@testing-library/react`, `@testing-library/jest-dom`
- Настроить `vitest.config.ts`
- Создать `src/__tests__/setup.ts` для глобальных настроек

### 6. Интеграция с Mock API

**Файл**: `src/lib/api.ts`

Создать API client:

```typescript
// Типы из Mock API
interface StatsResponse {
  overall: { total_dialogs: number; active_users: number; avg_dialog_length: number };
  activity_data: Array<{ timestamp: string; message_count: number }>;
  recent_dialogs: Array<{ user_id: number; last_message: string; created_at: string; message_count: number }>;
  top_users: Array<{ user_id: number; message_count: number; last_active: string }>;
  period: 'day' | 'week' | 'month';
}

// Функция для получения статистики
async function fetchStats(period: 'day' | 'week' | 'month'): Promise<StatsResponse>
```

**Конфигурация**: `src/config/api.config.ts`

```typescript
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const API_ENDPOINTS = {
  health: '/health',
  stats: '/stats',
};
```

**Environment variables**:

Создать `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Создать `.env.example` для документирования:

```
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 7. Команды разработки

**Обновить**: `frontend/package.json` scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

**Обновить**: Корневой `Makefile` - добавить команды для frontend

```makefile
# Frontend commands
.PHONY: frontend-install frontend-dev frontend-build frontend-lint frontend-test

frontend-install:
	cd frontend && pnpm install

frontend-dev:
	cd frontend && pnpm dev

frontend-build:
	cd frontend && pnpm build

frontend-lint:
	cd frontend && pnpm lint && pnpm format:check && pnpm type-check

frontend-test:
	cd frontend && pnpm test
```

### 8. Обновление документации

**Обновить**: `frontend/README.md`

Добавить секции:

- Технологический стек
- Требования к системе (Node.js 18+, pnpm)
- Установка зависимостей (`pnpm install`)
- Запуск dev-сервера (`pnpm dev`)
- Структура проекта
- Команды разработки
- Интеграция с Backend API
- Соглашения о кодировании

**Создать**: `frontend/.gitignore`

Игнорировать:

- `node_modules/`
- `.next/`
- `out/`
- `.env*.local`
- `coverage/`
- `.DS_Store`

### 9. Создание базового layout и заглушки Dashboard

**Файл**: `src/app/layout.tsx`

Root layout с:

- Метаданные приложения
- Подключение шрифтов
- Provider'ы (если нужны)

**Файл**: `src/app/page.tsx`

Простая заглушка Dashboard со структурой:

- Header с выбором периода
- 4 секции (Overall Stats, Activity Chart, Recent Dialogs, Top Users)
- Placeholder компоненты с mock данными для проверки

**Цель**: Убедиться что приложение запускается и базовый layout работает

### 10. Настройка CI/CD проверок

**Создать**: `.github/workflows/frontend-ci.yml` (если используется GitHub Actions)

Проверки:

- `pnpm install`
- `pnpm type-check`
- `pnpm lint`
- `pnpm format:check`
- `pnpm test`
- `pnpm build`

## Критерии приемки

- ✅ Next.js проект инициализирован в `frontend/` с TypeScript
- ✅ shadcn/ui настроен и базовые компоненты установлены
- ✅ Структура директорий организована согласно плану
- ✅ ESLint + Prettier + TypeScript настроены и работают
- ✅ Vitest настроен для тестирования
- ✅ API client создан и протипизирован для Mock API
- ✅ Environment variables настроены (`.env.local`)
- ✅ Команды `pnpm dev`, `pnpm build`, `pnpm lint`, `pnpm test` работают
- ✅ Makefile обновлен с frontend командами
- ✅ Frontend vision документ создан
- ✅ README.md обновлен с инструкциями
- ✅ Базовая страница Dashboard доступна на `http://localhost:3000`
- ✅ Нет linter/type ошибок при запуске проверок

## Важные замечания

1. **App Router**: Используем новый App Router Next.js 15, а не Pages Router
2. **TypeScript strict**: Все компоненты должны быть полностью типизированы
3. **shadcn/ui convention**: Компоненты из shadcn устанавливаются в `src/components/ui/`
4. **API integration**: Пока только Mock API (http://localhost:8000), переход на Real API в спринте F5
5. **Responsive design**: Все компоненты должны быть адаптивными (mobile-first)
6. **No state management library yet**: Начинаем с React hooks (useState, useEffect), при необходимости добавим Zustand/Jotai позже

## Связанные файлы

- `doc/dashboard-requirements.md` - функциональные требования к UI
- `doc/api-contract-example.json` - контракт API для типизации
- `src/api/app.py` - Mock API endpoints
- `docs/vision.md` - backend vision (референс для frontend vision)

## Следующий спринт

**F3: Реализация Dashboard** - полная реализация UI компонентов с визуализацией данных из Mock API

### To-dos

- [ ] Создать frontend/doc/front-vision.md с архитектурным видением
- [ ] Создать frontend/doc/adr-tech-stack.md с обоснованием выбора технологий
- [ ] Инициализировать Next.js проект с TypeScript и настроить pnpm
- [ ] Настроить shadcn/ui и установить базовые компоненты
- [ ] Настроить ESLint, Prettier, TypeScript strict mode, Vitest
- [ ] Создать структуру директорий и базовые файлы (api.ts, types.ts, config)
- [ ] Создать API client с типизацией для Mock API endpoints
- [ ] Создать .env.local и .env.example для переменных окружения
- [ ] Настроить package.json scripts и обновить Makefile
- [ ] Создать базовый layout и заглушку Dashboard страницы
- [ ] Обновить frontend/README.md и создать .gitignore
- [ ] Проверить что все команды в package.json работают (dev, build, lint, test)
- [ ] Тестировать подключение к Mock API (запустить make run-api и проверить fetchStats)
- [ ] Проверить отсутствие ошибок линтера/типов во всех файлах
- [ ] Актуализировать doc/frontend-roadmap.md - обновить статус спринта F2
- [ ] Добавить ссылку на план в таблицу спринтов в frontend-roadmap.md
