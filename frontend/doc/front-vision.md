# Техническое видение Frontend: Web-интерфейс для Telegram бота

## 1. Технологии

### Базовые технологии

- **Next.js 15** - React фреймворк с App Router для server-side rendering
- **TypeScript 5.x** - строгая типизация для предотвращения ошибок
- **React 18+** - библиотека для построения UI компонентов
- **pnpm** - быстрый и эффективный пакетный менеджер

### UI и стилизация

- **shadcn/ui** - коллекция переиспользуемых компонентов на базе Radix UI
- **Tailwind CSS 3.x** - utility-first CSS фреймворк
- **Radix UI** - headless UI примитивы с доступностью (a11y)
- **Lucide React** - иконки для интерфейса

### Визуализация данных

- **Recharts** - библиотека для построения графиков и диаграмм
- **date-fns** - утилиты для работы с датами

### Тестирование

- **Vitest** - быстрый unit test фреймворк
- **React Testing Library** - тестирование React компонентов
- **@testing-library/jest-dom** - дополнительные матчеры для DOM

### Инструменты качества кода

- **ESLint** - статический анализ кода с правилами Next.js и React
- **Prettier** - автоматическое форматирование кода
- **TypeScript** - type checking в strict mode

### API интеграция

- **Fetch API** - нативный HTTP клиент для запросов к backend
- **Environment variables** - конфигурация через `.env.local`

## 2. Принципы разработки

### Архитектурные принципы

- **Component-based architecture** - приложение состоит из переиспользуемых компонентов
- **Separation of Concerns** - разделение UI, бизнес-логики и data fetching
- **Server-first approach** - использование Server Components где возможно
- **Progressive Enhancement** - базовая функциональность работает без JavaScript

### Принципы кода

- **Typed everything** - TypeScript strict mode, все компоненты типизированы
- **Single Responsibility** - каждый компонент отвечает за одну задачу
- **Composition over Inheritance** - композиция компонентов вместо наследования
- **Props drilling avoidance** - использование hooks для управления состоянием
- **Explicit over Implicit** - явные пропсы и типы вместо неявного поведения
- **DRY (Don't Repeat Yourself)** - переиспользование кода через хуки и компоненты

### Подход к разработке

- **Mobile-first** - сначала разрабатываем для мобильных устройств
- **Accessibility** - поддержка screen readers и keyboard navigation
- **Performance** - оптимизация bundle size и loading time
- **Iterative development** - от простого к сложному, MVP сначала
- **Type safety** - никаких `any`, использование строгих типов
- **Test coverage** - критичные компоненты покрыты тестами (>= 70%)

## 3. Структура проекта

```
frontend/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx           # Root layout с metadata
│   │   ├── page.tsx             # Home page (Dashboard)
│   │   ├── globals.css          # Global styles
│   │   └── favicon.ico          # Favicon
│   ├── components/              # React компоненты
│   │   ├── ui/                  # shadcn/ui базовые компоненты
│   │   │   ├── card.tsx
│   │   │   ├── button.tsx
│   │   │   ├── select.tsx
│   │   │   └── table.tsx
│   │   ├── dashboard/           # Dashboard специфичные компоненты
│   │   │   ├── OverallStats.tsx      # Карточки с общей статистикой
│   │   │   ├── ActivityChart.tsx     # График активности
│   │   │   ├── RecentDialogs.tsx     # Список последних диалогов
│   │   │   ├── TopUsers.tsx          # Топ пользователей
│   │   │   └── PeriodSelector.tsx    # Выбор периода (day/week/month)
│   │   └── layout/              # Layout компоненты
│   │       ├── Header.tsx       # Header приложения
│   │       └── Footer.tsx       # Footer (опционально)
│   ├── lib/                     # Утилиты и хелперы
│   │   ├── utils.ts             # shadcn/ui cn() и другие утилиты
│   │   ├── api.ts               # API client для backend
│   │   └── types.ts             # TypeScript типы и интерфейсы
│   ├── hooks/                   # Custom React hooks
│   │   ├── useStats.ts          # Hook для получения статистики
│   │   └── useMediaQuery.ts     # Hook для responsive design (опционально)
│   └── config/                  # Конфигурация
│       └── api.config.ts        # API endpoints и настройки
├── public/                      # Статические файлы
│   └── images/                  # Изображения
├── doc/                         # Документация
│   ├── front-vision.md          # Этот файл
│   ├── adr-tech-stack.md        # Architecture Decision Record
│   └── plans/                   # Планы спринтов
│       └── s2-init-plan.md
├── .env.local                   # Environment variables (не в git)
├── .env.example                 # Пример переменных окружения
├── .gitignore                   # Git ignore
├── .prettierrc                  # Prettier конфигурация
├── components.json              # shadcn/ui конфигурация
├── eslint.config.mjs            # ESLint конфигурация
├── next.config.ts               # Next.js конфигурация
├── package.json                 # NPM dependencies и scripts
├── pnpm-lock.yaml               # pnpm lock file
├── postcss.config.mjs           # PostCSS конфигурация
├── tailwind.config.ts           # Tailwind CSS конфигурация
├── tsconfig.json                # TypeScript конфигурация
├── vitest.config.ts             # Vitest конфигурация
└── README.md                    # Frontend документация
```

## 4. Организация компонентов

### Категории компонентов

#### UI Components (`components/ui/`)

- Базовые переиспользуемые компоненты от shadcn/ui
- Не содержат бизнес-логики
- Полностью controlled (управляются через props)
- Примеры: Button, Card, Select, Table

#### Feature Components (`components/dashboard/`)

- Компоненты специфичные для Dashboard
- Содержат бизнес-логику для визуализации статистики
- Используют UI компоненты для построения интерфейса
- Примеры: OverallStats, ActivityChart, RecentDialogs

#### Layout Components (`components/layout/`)

- Компоненты для общего layout приложения
- Header, Footer, Sidebar (если будет)
- Навигация между страницами (в будущих спринтах)

### Структура компонента

```typescript
// Импорты
import { FC } from 'react';
import { Card } from '@/components/ui/card';

// Типы Props
interface ComponentProps {
  data: SomeType;
  onAction?: () => void;
}

// Компонент
export const Component: FC<ComponentProps> = ({ data, onAction }) => {
  // Hooks
  // State
  // Effects
  // Handlers

  // Render
  return (
    <Card>
      {/* JSX */}
    </Card>
  );
};
```

## 5. State Management

### Локальное состояние

- **useState** - для локального state компонента
- **useReducer** - для сложной логики с множественными transitions
- **useContext** - для sharing state между компонентами (если нужно)

### Server State

- **React Server Components** - для данных, fetched на сервере
- **useEffect + fetch** - для client-side data fetching (Dashboard данные)
- Custom hooks (`useStats`) - для инкапсуляции data fetching логики

### Будущее (если понадобится)

- **Zustand** или **Jotai** - для глобального state management
- **React Query** - для server state management с кешированием

## 6. Интеграция с Backend API

### Этапы интеграции

#### Этап 1: Mock API (Спринты F2-F4)

- Backend предоставляет Mock API с тестовыми данными
- URL: `http://localhost:8000`
- Endpoints:
  - `GET /health` - health check
  - `GET /stats?period={day|week|month}` - статистика

#### Этап 2: Real API (Спринт F5)

- Переключение с Mock на Real реализацию StatCollector
- Те же endpoints, но с реальными данными из БД
- Без изменений в frontend коде (только env variables)

### API Client структура

```typescript
// src/lib/api.ts
export const apiClient = {
  async getStats(period: Period): Promise<StatsResponse> {
    const response = await fetch(`${API_BASE_URL}/stats?period=${period}`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  },

  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  },
};
```

### Типизация API responses

```typescript
// src/lib/types.ts
export type Period = 'day' | 'week' | 'month';

export interface StatsResponse {
  overall: {
    total_dialogs: number;
    active_users: number;
    avg_dialog_length: number;
  };
  activity_data: ActivityDataPoint[];
  recent_dialogs: RecentDialog[];
  top_users: TopUser[];
  period: Period;
}

// ... другие типы
```

## 7. Соглашения о стилях и UI/UX

### Styling подход

- **Tailwind CSS** - для всех стилей
- **CSS Variables** - для темизации (dark/light mode)
- **Mobile-first** - медиа-запросы от меньшего к большему
- **Responsive breakpoints**:
  - `sm`: 640px (mobile)
  - `md`: 768px (tablet)
  - `lg`: 1024px (desktop)
  - `xl`: 1280px (large desktop)

### UI Guidelines

- **Spacing**: использовать Tailwind spacing scale (4, 8, 12, 16, 24, 32px)
- **Colors**: использовать Tailwind color palette + shadcn/ui semantic colors
- **Typography**: использовать Tailwind typography utilities
- **Borders**: border-radius от Tailwind (rounded-md, rounded-lg)
- **Shadows**: elevation через Tailwind shadow utilities

### Accessibility (a11y)

- **Semantic HTML** - использовать правильные HTML теги
- **ARIA attributes** - для интерактивных элементов
- **Keyboard navigation** - все действия доступны с клавиатуры
- **Focus management** - видимый focus ring на элементах
- **Color contrast** - минимум WCAG AA для текста

### UX Guidelines

- **Loading states** - показывать loading indicators при загрузке
- **Error handling** - понятные сообщения об ошибках
- **Empty states** - placeholder когда нет данных
- **Responsive design** - адаптация под все размеры экранов
- **Performance** - быстрая загрузка и smooth transitions

## 8. Testing Strategy

### Unit Tests

- **Vitest + React Testing Library**
- Тестировать изолированные компоненты
- Фокус на пользовательском поведении, не на implementation details
- Примеры:
  - Button clicks
  - Form submissions
  - Data rendering
  - Conditional rendering

### Integration Tests (будущее)

- **Playwright** или **Cypress**
- End-to-end тесты критичных user flows
- Тестирование с Mock API

### Test Coverage цели

- **Critical components**: >= 80%
- **UI components**: >= 70%
- **Utils/helpers**: >= 90%

## 9. Performance Optimization

### Next.js оптимизации

- **Server Components** - render на сервере где возможно
- **Code splitting** - автоматически через Next.js
- **Image optimization** - использовать `next/image`
- **Font optimization** - использовать `next/font`

### Bundle optimization

- **Tree shaking** - удаление неиспользуемого кода
- **Dynamic imports** - для больших компонентов
- **Lazy loading** - для non-critical компонентов

### Runtime optimization

- **Memoization** - `useMemo`, `useCallback` для дорогих вычислений
- **Virtualization** - для длинных списков (если понадобится)
- **Debouncing** - для частых событий (поиск, resize)

## 10. Development Workflow

### Локальная разработка

1. `pnpm install` - установка зависимостей
2. `pnpm dev` - запуск dev-сервера (http://localhost:3000)
3. Редактирование кода с hot reload
4. `pnpm lint` - проверка кода линтером
5. `pnpm type-check` - проверка типов TypeScript
6. `pnpm test` - запуск тестов

### Before commit

1. `pnpm format` - форматирование кода
2. `pnpm lint:fix` - автофикс линтер ошибок
3. `pnpm type-check` - проверка типов
4. `pnpm test` - прогон тестов

### Build and deploy

1. `pnpm build` - production build
2. `pnpm start` - запуск production сервера
3. Deploy на hosting (Vercel, Netlify, или self-hosted)

## 11. Future Enhancements

### Спринт F3: Dashboard реализация

- Полная реализация всех компонентов Dashboard
- Интеграция с Mock API
- Responsive design для всех устройств
- Unit тесты для компонентов

### Спринт F4: ИИ-чат

- Веб-чат компонент для общения с ботом
- Интеграция с text-to-SQL функционалом
- Real-time messaging (WebSocket или polling)
- История диалогов в чате

### Спринт F5: Real API

- Переключение с Mock на Real API
- Реальная статистика из БД
- Оптимизация запросов
- Caching стратегия

### Будущие возможности

- **Dark mode** - тема оформления
- **Multi-language** - интернационализация (i18n)
- **User authentication** - авторизация админа
- **Real-time updates** - WebSocket для live статистики
- **Export data** - экспорт в CSV/Excel
- **Advanced filtering** - фильтры по пользователям, датам
- **Analytics dashboard** - расширенная аналитика

## 12. Связанные документы

- [Dashboard Requirements](../doc/dashboard-requirements.md) - функциональные требования
- [Frontend Roadmap](../doc/frontend-roadmap.md) - план развития
- [Backend Vision](../../docs/vision.md) - техническое видение backend
- [ADR Tech Stack](./adr-tech-stack.md) - обоснование выбора технологий
- [Sprint F2 Plan](./plans/s2-init-plan.md) - план спринта инициализации

---

**Версия**: 1.0
**Дата создания**: 2025-10-17
**Последнее обновление**: 2025-10-17
**Статус**: Утверждено
