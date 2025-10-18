<!-- f40776af-e269-4d1a-86de-35e07eacacfb 081013e3-1ef0-4419-a41d-fa8f6951b52e -->
# Sprint F3: Реализация Dashboard статистики диалогов

## Обзор

Создание полнофункционального дашборда с визуализацией статистики диалогов Telegram-бота на основе дизайна shadcn/ui Dashboard-01. Интеграция с Mock API, responsive design, loading/error states и unit-тесты.

## Текущее состояние

**Готово из Sprint F2:**

- ✅ Next.js 15 + TypeScript инфраструктура
- ✅ shadcn/ui компоненты: `card`, `button`, `select`, `table`
- ✅ API client (`src/lib/api.ts`) и типы (`src/lib/types.ts`)
- ✅ Базовая страница с placeholder компонентами
- ✅ Mock API на `http://localhost:8000`

**Отсутствует:**

- Dashboard компоненты (директория `src/components/dashboard/` пустая)
- Библиотека для графиков (Recharts)
- Hook для data fetching (`useStats`)
- Реальная интеграция с API
- Loading/error states

## Этап 1: Установка зависимостей

### 1.1 Установить Recharts для графиков

```bash
cd frontend && pnpm add recharts date-fns
```

**Зависимости:**

- `recharts` - библиотека для построения графиков активности
- `date-fns` - утилиты для форматирования дат и времени

## Этап 2: Custom Hook для работы с API

### 2.1 Создать `src/hooks/useStats.ts`

**Функционал:**

- Загрузка статистики через `apiClient.getStats(period)`
- Управление состояниями: `loading`, `error`, `data`
- Автоматическая перезагрузка при изменении периода
- Обработка ошибок сети

**Структура:**

```typescript
export function useStats(initialPeriod: Period = 'day') {
  const [period, setPeriod] = useState<Period>(initialPeriod);
  const [data, setData] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch logic with error handling
  }, [period]);

  return { data, loading, error, period, setPeriod };
}
```

**Тестовое покрытие:** Mock fetch, проверка всех состояний

## Этап 3: Dashboard компоненты

### 3.1 PeriodSelector компонент

**Файл:** `src/components/dashboard/PeriodSelector.tsx`

**Функционал:**

- 3 кнопки для выбора периода: День / Неделя / Месяц
- Визуальное выделение активного периода
- Callback для изменения периода

**UI:** Группа из 3 кнопок с использованием `Button` компонента, variant `default` для активной, `outline` для остальных

**Props:**

```typescript
interface PeriodSelectorProps {
  period: Period;
  onPeriodChange: (period: Period) => void;
}
```

### 3.2 OverallStats компонент

**Файл:** `src/components/dashboard/OverallStats.tsx`

**Функционал:**

- Отображение 3 карточек метрик в горизонтальный ряд
- Адаптивный grid (1 колонка на mobile, 3 на desktop)
- Метрики: Всего диалогов, Активных пользователей, Средняя длина диалога

**UI:**

- Использование `Card`, `CardHeader`, `CardTitle`, `CardContent`
- Крупные числа (text-2xl font-bold)
- Подписи под метриками (text-muted-foreground text-xs)

**Props:**

```typescript
interface OverallStatsProps {
  stats: OverallStats;
}
```

**Референс:** shadcn/ui Dashboard-01 верхние карточки

### 3.3 ActivityChart компонент

**Файл:** `src/components/dashboard/ActivityChart.tsx`

**Функционал:**

- График активности пользователей во времени
- Использование Recharts (LineChart или AreaChart)
- Адаптация оси X в зависимости от периода:
  - Day: часы (0-23)
  - Week: дни недели (Пн-Вс)
  - Month: даты (1-30)
- Форматирование timestamp с помощью `date-fns`
- Responsive design (высота 300-400px)

**UI:**

- Обернуто в `Card` компонент
- Tooltip при наведении на точку графика
- Gradients для area fill (опционально)

**Props:**

```typescript
interface ActivityChartProps {
  data: ActivityDataPoint[];
  period: Period;
}
```

**Референс:** shadcn/ui Dashboard-01 центральный график

### 3.4 RecentDialogs компонент

**Файл:** `src/components/dashboard/RecentDialogs.tsx`

**Функционал:**

- Таблица последних 10 диалогов
- Колонки: User ID, Превью сообщения, Дата создания, Кол-во сообщений
- Truncate длинных сообщений (max 100 символов + "...")
- Форматирование даты в читаемый формат (date-fns)

**UI:**

- Использование shadcn/ui `Table` компонента
- Responsive: на mobile скрывать некоторые колонки или переключиться на Card list
- Alternating row colors для читаемости

**Props:**

```typescript
interface RecentDialogsProps {
  dialogs: RecentDialog[];
}
```

**Референс:** shadcn/ui Dashboard-01 таблица транзакций

### 3.5 TopUsers компонент

**Файл:** `src/components/dashboard/TopUsers.tsx`

**Функционал:**

- Список топ 5 активных пользователей
- Информация: User ID, количество сообщений, последняя активность
- Сортировка по убыванию message_count (уже отсортировано с backend)
- Относительное время последней активности ("2 часа назад")

**UI:**

- Карточки или список с border между элементами
- Flex layout: user info слева, метрики справа
- Badge для номера места (1, 2, 3, 4, 5) - опционально

**Props:**

```typescript
interface TopUsersProps {
  users: TopUser[];
}
```

**Референс:** shadcn/ui Dashboard-01 список recent sales

## Этап 4: Интеграция компонентов в главную страницу

### 4.1 Обновить `src/app/page.tsx`

**Изменения:**

- Преобразовать в Client Component (`'use client'`)
- Использовать `useStats` hook для загрузки данных
- Заменить placeholder компоненты на реальные
- Добавить loading state (skeleton или spinner)
- Добавить error state (сообщение об ошибке с retry кнопкой)
- Добавить empty state (если данных нет)

**Layout структура:**

```tsx
<div className="container mx-auto p-8">
  <Header />
  <PeriodSelector period={period} onPeriodChange={setPeriod} />
  
  {loading && <LoadingState />}
  {error && <ErrorState error={error} onRetry={retry} />}
  {data && (
    <>
      <OverallStats stats={data.overall} />
      <ActivityChart data={data.activity_data} period={period} />
      <div className="grid md:grid-cols-2 gap-6">
        <RecentDialogs dialogs={data.recent_dialogs} />
        <TopUsers users={data.top_users} />
      </div>
    </>
  )}
</div>
```

## Этап 5: Responsive Design

### 5.1 Применить адаптивность

**Breakpoints (Tailwind):**

- Mobile: default (< 640px)
- Tablet: `md:` (≥ 768px)
- Desktop: `lg:` (≥ 1024px)

**Адаптации:**

- OverallStats: `grid-cols-1 md:grid-cols-3`
- ActivityChart: динамическая высота и width 100%
- RecentDialogs + TopUsers: `grid md:grid-cols-2`
- На mobile таблицу превратить в карточки (опционально)

### 5.2 Тестирование на разных экранах

Проверить отображение:

- iPhone SE (375px)
- iPad (768px)
- Desktop (1280px+)

## Этап 6: Loading и Error States

### 6.1 Loading State компоненты

**Опции:**

1. **Skeleton screens** - использовать shadcn/ui skeleton (если есть) или создать простые placeholder'ы
2. **Spinner** - центрированный loading spinner

**Реализация:**

```tsx
function LoadingState() {
  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-3 gap-4">
        {[1, 2, 3].map(i => (
          <Card key={i}>
            <CardContent className="h-24 animate-pulse bg-muted" />
          </Card>
        ))}
      </div>
      <Card>
        <CardContent className="h-[400px] animate-pulse bg-muted" />
      </Card>
    </div>
  );
}
```

### 6.2 Error State компонент

**Функционал:**

- Отображение сообщения об ошибке
- Кнопка "Повторить попытку" для retry
- Иконка ошибки (из lucide-react)

**Реализация:**

```tsx
function ErrorState({ error, onRetry }: { error: string; onRetry: () => void }) {
  return (
    <Card className="p-8 text-center">
      <AlertCircle className="mx-auto h-12 w-12 text-destructive" />
      <h3 className="mt-4 text-lg font-semibold">Ошибка загрузки данных</h3>
      <p className="text-muted-foreground mt-2">{error}</p>
      <Button onClick={onRetry} className="mt-4">
        Повторить попытку
      </Button>
    </Card>
  );
}
```

### 6.3 Empty State (опционально)

Если статистика пустая (0 диалогов), показать friendly сообщение.

## Этап 7: Утилиты и хелперы

### 7.1 Создать `src/lib/format.ts`

**Функции:**

- `formatDate(isoString: string): string` - форматирование даты
- `formatRelativeTime(isoString: string): string` - "2 часа назад"
- `formatNumber(num: number): string` - форматирование больших чисел
- `truncateText(text: string, maxLength: number): string` - обрезка текста

**Пример:**

```typescript
import { format, formatDistanceToNow, parseISO } from 'date-fns';
import { ru } from 'date-fns/locale';

export function formatDate(isoString: string): string {
  return format(parseISO(isoString), 'dd MMM yyyy, HH:mm', { locale: ru });
}

export function formatRelativeTime(isoString: string): string {
  return formatDistanceToNow(parseISO(isoString), { addSuffix: true, locale: ru });
}
```

### 7.2 Настроить русскую локализацию date-fns

Импортировать `ru` locale из `date-fns/locale` для корректного отображения дат на русском языке.

## Этап 8: Тестирование

### 8.1 Unit-тесты для useStats hook

**Файл:** `src/hooks/__tests__/useStats.test.ts`

**Тесты:**

- ✅ Загрузка данных при монтировании
- ✅ Изменение периода перезагружает данные
- ✅ Обработка ошибок API
- ✅ Loading state управление

### 8.2 Unit-тесты для компонентов

**Файлы:**

- `src/components/dashboard/__tests__/PeriodSelector.test.tsx`
- `src/components/dashboard/__tests__/OverallStats.test.tsx`
- `src/components/dashboard/__tests__/RecentDialogs.test.tsx`
- `src/components/dashboard/__tests__/TopUsers.test.tsx`

**Тесты:**

- ✅ Рендеринг с mock данными
- ✅ Обработка пустых данных
- ✅ Взаимодействия (клики, изменения)
- ✅ Форматирование данных

### 8.3 Integration тест для Dashboard page

**Файл:** `src/app/__tests__/page.test.tsx`

**Тесты:**

- ✅ Полный flow: loading → data → render
- ✅ Переключение периода
- ✅ Error handling и retry

### 8.4 Запуск тестов

```bash
pnpm test
pnpm test:coverage  # Проверить coverage >= 70%
```

## Этап 9: Финализация и документация

### 9.1 Проверить качество кода

```bash
pnpm type-check   # TypeScript errors
pnpm lint         # ESLint
pnpm format:check # Prettier
pnpm build        # Production build
```

Убедиться что:

- ✅ 0 TypeScript errors
- ✅ 0 ESLint warnings
- ✅ Production build успешен
- ✅ Bundle size разумный (< 200KB First Load)

### 9.2 Обновить документацию

**Файл:** `frontend/README.md`

Добавить секцию:

- Описание Dashboard компонентов
- Примеры использования `useStats` hook
- Скриншоты Dashboard (опционально)

**Файл:** `doc/frontend-roadmap.md`

Обновить статус:

- F3: 🔵 Запланировано → 🟢 Завершено
- Добавить ссылку на план

### 9.3 Создать Sprint Summary

**Файл:** `SPRINT_F3_SUMMARY.md`

Структура:

- Результаты спринта
- Созданные компоненты
- Статистика (строк кода, файлов)
- Команды для запуска
- Скриншоты (если возможно)
- Следующие шаги

## Критерии приёмки

### Функциональные

- ✅ PeriodSelector переключает между day/week/month
- ✅ OverallStats отображает 3 метрики корректно
- ✅ ActivityChart рисует график активности (Recharts)
- ✅ RecentDialogs показывает последние 10 диалогов
- ✅ TopUsers отображает топ 5 пользователей
- ✅ Данные загружаются из Mock API (`http://localhost:8000`)
- ✅ При изменении периода данные перезагружаются
- ✅ Loading state отображается при загрузке
- ✅ Error state с retry кнопкой при ошибке

### Технические

- ✅ Все компоненты типизированы (TypeScript strict mode)
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ 0 TypeScript errors
- ✅ 0 ESLint warnings
- ✅ Test coverage >= 70% для критичных компонентов
- ✅ Production build проходит успешно
- ✅ Форматирование дат на русском языке
- ✅ API интеграция работает с Mock API

### Документация

- ✅ README обновлён с описанием компонентов
- ✅ Roadmap обновлён (F3 статус)
- ✅ Sprint Summary создан

## Важные замечания

1. **Референс дизайна:** Следовать стилю [shadcn/ui Dashboard-01](https://ui.shadcn.com/blocks#dashboard-01)
2. **API контракт:** Использовать структуру из `doc/api-contract-example.json`
3. **Русская локализация:** Все даты и числа форматировать на русском
4. **Mobile-first:** Разрабатывать сначала для мобильных устройств
5. **TypeScript strict:** Никаких `any`, полная типизация
6. **Client Components:** Dashboard использует hooks, значит нужен `'use client'`
7. **Recharts документация:** [recharts.org](https://recharts.org) для примеров графиков

## Связанные файлы

- `doc/dashboard-requirements.md` - функциональные требования
- `doc/api-contract-example.json` - структура данных API
- `frontend/doc/front-vision.md` - техническое видение
- `frontend/src/lib/types.ts` - TypeScript типы (уже готовы)
- `frontend/src/lib/api.ts` - API client (уже готов)

## Следующий спринт

**F4: Реализация ИИ-чата** - веб-интерфейс для общения с ботом через natural language queries

---

**Оценка времени:** 6-8 часов

**Файлов для создания:** ~15

**Строк кода:** ~800-1000

### To-dos

- [ ] Установить recharts и date-fns для графиков и форматирования дат
- [ ] Создать custom hook useStats для загрузки статистики с API
- [ ] Реализовать компонент PeriodSelector для выбора периода
- [ ] Реализовать компонент OverallStats с карточками метрик
- [ ] Реализовать компонент ActivityChart с графиком на Recharts
- [ ] Реализовать компонент RecentDialogs с таблицей диалогов
- [ ] Реализовать компонент TopUsers со списком активных пользователей
- [ ] Создать утилиты для форматирования дат и чисел (src/lib/format.ts)
- [ ] Интегрировать все компоненты в src/app/page.tsx с loading/error states
- [ ] Применить responsive design и протестировать на разных экранах
- [ ] Написать unit-тесты для компонентов и useStats hook
- [ ] Обновить документацию (README, roadmap) и создать Sprint Summary