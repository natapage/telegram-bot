# ADR: Выбор технологического стека для Frontend

> **Architecture Decision Record**
> **Дата**: 2025-10-17
> **Статус**: Утверждено
> **Контекст**: Инициализация frontend проекта для веб-интерфейса Telegram бота

---

## Контекст и проблема

Необходимо выбрать оптимальный технологический стек для разработки веб-интерфейса с дашбордом статистики и ИИ-чатом. Требования:

- Быстрая разработка и итерация
- Type safety для предотвращения ошибок
- Современный UI с готовыми компонентами
- Хорошая производительность
- Простота поддержки и масштабирования
- Совместимость с backend Python + FastAPI

---

## Решения по технологиям

### 1. Framework: Next.js 15 (App Router)

#### Выбор

**Next.js 15** с новым App Router

#### Альтернативы рассмотрены

- **Create React App (CRA)** - устаревший, не поддерживается
- **Vite + React** - хороший вариант, но без SSR из коробки
- **Remix** - современный, но меньше ecosystem
- **Vue.js/Nuxt** - отличный выбор, но команда больше знакома с React
- **Svelte/SvelteKit** - инновационный, но меньше ресурсов для обучения

#### Обоснование выбора Next.js 15

**Преимущества:**

- ✅ **Server Components** - рендеринг на сервере для лучшей производительности
- ✅ **App Router** - современная файловая маршрутизация с nested layouts
- ✅ **Built-in оптимизации** - автоматический code splitting, image optimization
- ✅ **SEO friendly** - SSR из коробки
- ✅ **Большой ecosystem** - огромное количество библиотек и примеров
- ✅ **Vercel deploy** - одна команда для деплоя
- ✅ **TypeScript first** - отличная поддержка TypeScript
- ✅ **Документация** - исчерпывающая и актуальная

**Недостатки:**

- ❌ **Complexity** - более сложен чем простой Vite + React
- ❌ **Learning curve** - App Router новый, требует изучения
- ❌ **Over-engineering** - для простого SPA может быть избыточным

**Почему именно App Router, а не Pages Router:**

- App Router - это будущее Next.js
- Server Components - значительное улучшение производительности
- Nested layouts - лучше для сложных приложений
- Pages Router в legacy mode

**Trade-offs:**

- Принимаем сложность Next.js взамен на мощные возможности SSR и оптимизации
- Для нашего случая (Dashboard с API integration) это оправдано

---

### 2. Язык: TypeScript 5.x (strict mode)

#### Выбор

**TypeScript 5.x** в strict mode

#### Альтернативы рассмотрены

- **JavaScript (JSX)** - без типизации
- **TypeScript non-strict** - частичная типизация
- **Flow** - альтернативный type checker от Facebook (deprecated)

#### Обоснование выбора TypeScript strict

**Преимущества:**

- ✅ **Type safety** - ошибки ловятся на этапе разработки
- ✅ **Better IDE support** - автокомплит, refactoring, navigation
- ✅ **Self-documenting code** - типы как документация
- ✅ **Refactoring confidence** - изменения без страха что-то сломать
- ✅ **Backend contract** - типы совпадают с API контрактом
- ✅ **Team productivity** - меньше runtime ошибок
- ✅ **Industry standard** - используется в большинстве проектов

**Недостатки:**

- ❌ **Initial setup** - требует настройки tsconfig.json
- ❌ **Learning curve** - нужно знать систему типов
- ❌ **Build time** - type checking добавляет время сборки

**Почему strict mode:**

- Максимальная защита от ошибок
- Запрещает `any` и неявные типы
- Лучше сразу писать правильно, чем потом исправлять

**Trade-offs:**

- Немного больше времени на написание типов, но значительно меньше багов

---

### 3. UI Library: shadcn/ui

#### Выбор

**shadcn/ui** (с Radix UI под капотом)

#### Альтернативы рассмотрены

- **Material-UI (MUI)** - самая популярная, но тяжелая
- **Ant Design** - много компонентов, но китайский дизайн
- **Chakra UI** - хороший, но менее гибкий
- **Mantine** - современный, но меньше adoption
- **Headless UI** - низкоуровневый, требует больше работы
- **Построить с нуля** - полный контроль, но очень долго

#### Обоснование выбора shadcn/ui

**Преимущества:**

- ✅ **Copy-paste approach** - компоненты копируются в проект, полный контроль
- ✅ **Customizable** - легко модифицировать под нужды
- ✅ **Radix UI primitives** - качественная основа с a11y
- ✅ **Tailwind CSS** - идеально интегрируется с Tailwind
- ✅ **TypeScript first** - все компоненты типизированы
- ✅ **Modern design** - актуальный внешний вид
- ✅ **No bundle bloat** - используешь только то, что нужно
- ✅ **CLI для установки** - `npx shadcn@latest add component`
- ✅ **Dashboard templates** - готовые референсы (Dashboard-01)

**Недостатки:**

- ❌ **Not a library** - компоненты живут в твоем коде
- ❌ **Updates вручную** - нужно обновлять компоненты самостоятельно
- ❌ **Less components** - меньше готовых компонентов чем в MUI

**Почему не Material-UI:**

- MUI тяжелый (large bundle size)
- Сложная кастомизация темы
- Material Design не всегда подходит

**Почему не Ant Design:**

- Специфичный китайский дизайн
- Сложно изменить визуальный стиль

**Trade-offs:**

- Меньше готовых компонентов, но полный контроль и легкая кастомизация
- Для Dashboard с 4-5 компонентами это идеально

---

### 4. Styling: Tailwind CSS 3.x

#### Выбор

**Tailwind CSS 3.x**

#### Альтернативы рассмотрены

- **CSS Modules** - традиционный подход
- **Styled Components** - CSS-in-JS
- **Emotion** - альтернативный CSS-in-JS
- **Vanilla CSS** - обычный CSS
- **Sass/SCSS** - препроцессор

#### Обоснование выбора Tailwind CSS

**Преимущества:**

- ✅ **Utility-first** - быстрая разработка
- ✅ **No naming** - не нужно придумывать имена классов
- ✅ **Consistent design system** - единый spacing/colors из коробки
- ✅ **Responsive design** - легкие медиа-запросы
- ✅ **Small bundle** - unused classes удаляются (PurgeCSS)
- ✅ **Dark mode** - встроенная поддержка dark mode
- ✅ **Great DX** - автокомплит в IDE с расширениями
- ✅ **Industry adoption** - используется в большинстве современных проектов

**Недостатки:**

- ❌ **Verbose HTML** - много классов в JSX
- ❌ **Learning curve** - нужно знать утилиты
- ❌ **Non-semantic** - классы не семантичные

**Почему не CSS-in-JS (Styled Components):**

- Runtime overhead - CSS генерируется во время исполнения
- Сложнее с SSR
- Larger bundle size

**Trade-offs:**

- Более длинный JSX, но значительно быстрее разработка и консистентный дизайн

---

### 5. Пакетный менеджер: pnpm

#### Выбор

**pnpm**

#### Альтернативы рассмотрены

- **npm** - стандартный, медленный
- **yarn** - быстрее npm, но устаревший
- **yarn berry (v2+)** - новый yarn, нестабильный
- **bun** - очень быстрый, но еще молодой

#### Обоснование выбора pnpm

**Преимущества:**

- ✅ **Fast** - быстрее npm и yarn
- ✅ **Disk efficient** - shared store, экономит место
- ✅ **Strict** - правильное разрешение зависимостей
- ✅ **Monorepo support** - если понадобится
- ✅ **Drop-in replacement** - совместим с npm/yarn
- ✅ **Stable** - production ready

**Недостатки:**

- ❌ **Less popular** - чем npm/yarn
- ❌ **CI setup** - нужно устанавливать в CI

**Почему не npm:**

- Медленный
- Занимает много места на диске

**Почему не yarn:**

- pnpm быстрее и эффективнее
- yarn classic (v1) больше не развивается

**Trade-offs:**

- Небольшие различия в командах, но значительный прирост скорости

---

### 6. Testing: Vitest

#### Выбор

**Vitest**

#### Альтернативы рассмотрены

- **Jest** - industry standard
- **Testing Library без runner** - нужен отдельный test runner
- **Mocha + Chai** - старый подход

#### Обоснование выбора Vitest

**Преимущества:**

- ✅ **Vite-powered** - использует Vite для быстрой сборки
- ✅ **Fast** - быстрее Jest в несколько раз
- ✅ **Jest-compatible API** - знакомый API
- ✅ **ESM first** - нативная поддержка ES modules
- ✅ **TypeScript support** - отличная работа с TS
- ✅ **UI mode** - визуальный интерфейс для тестов
- ✅ **Watch mode** - умный пересчет тестов

**Недостатки:**

- ❌ **Newer** - меньше adoption чем Jest
- ❌ **Less plugins** - меньше экосистемы

**Почему не Jest:**

- Медленнее Vitest
- Проблемы с ESM
- Требует больше конфигурации для TypeScript

**Trade-offs:**

- Меньше ресурсов для обучения, но значительно быстрее выполнение тестов

---

## Итоговый стек

```
Framework:        Next.js 15 (App Router)
Language:         TypeScript 5.x (strict mode)
UI Library:       shadcn/ui + Radix UI
Styling:          Tailwind CSS 3.x
Package Manager:  pnpm
Testing:          Vitest + React Testing Library
Linting:          ESLint + Prettier
```

---

## Критерии успеха выбранного стека

### Производительность

- ✅ Bundle size < 200KB (gzipped)
- ✅ First Contentful Paint < 1.5s
- ✅ Time to Interactive < 3s

### Developer Experience

- ✅ Hot reload < 200ms
- ✅ Type checking < 5s
- ✅ Test execution < 10s для всех тестов

### Maintainability

- ✅ Type safety - 100% типизированного кода
- ✅ Test coverage >= 70%
- ✅ Linter errors = 0

---

## Риски и митигации

### Риск 1: Сложность Next.js App Router

- **Вероятность**: Средняя
- **Влияние**: Среднее
- **Митигация**: Изучение документации, использование примеров, постепенное освоение

### Риск 2: shadcn/ui обновления

- **Вероятность**: Низкая
- **Влияние**: Низкое
- **Митигация**: Компоненты в нашем коде, полный контроль

### Риск 3: pnpm в CI/CD

- **Вероятность**: Низкая
- **Влияние**: Низкое
- **Митигация**: Простая установка в CI, хорошая документация

---

## Возможность изменения

Этот стек является рекомендацией, но не догмой. Если в процессе разработки выявятся критичные проблемы, стек может быть пересмотрен.

### Когда можно менять:

- Критичные performance issues
- Блокеры в разработке
- Значительные проблемы с поддержкой

### Что сложно поменять:

- Next.js → другой framework (полная переработка)
- TypeScript → JavaScript (потеря type safety)

### Что легко поменять:

- pnpm → npm/yarn (просто другие команды)
- Vitest → Jest (совместимый API)
- shadcn/ui → другая UI library (замена компонентов)

---

## Связанные документы

- [Frontend Vision](./front-vision.md) - техническое видение
- [Sprint F2 Plan](./plans/s2-init-plan.md) - план инициализации
- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

---

**Утверждено**: 2025-10-17
**Автор**: AI Agent
**Ревью**: Команда проекта
**Следующий пересмотр**: После спринта F3
