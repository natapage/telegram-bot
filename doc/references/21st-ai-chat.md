# AI Chat Component Reference

> **Источник**: 21st.dev
> **Назначение**: Референс для реализации UI компонента веб-чата в Спринте F4
> **Дата добавления**: 2025-10-17
> **Статус**: Готов к интеграции

---

## Обзор

Интерактивный компонент AI чата с современным дизайном, анимациями и визуальными эффектами. Компонент предоставляет полнофункциональный интерфейс для общения с AI-ассистентом с поддержкой истории сообщений и индикации набора текста.

### Ключевые особенности

- **Современный дизайн**: Темная тема с градиентами и эффектом glass-morphism
- **Плавные анимации**: Использование Framer Motion для transitions и эффектов
- **Анимированный бордер**: Вращающаяся граница вокруг карточки
- **Плавающие частицы**: Фоновая анимация с движущимися точками
- **Typing indicator**: Визуальная индикация когда AI "печатает" ответ
- **Responsive дизайн**: Адаптивная верстка для различных устройств
- **TypeScript**: Полная типизация компонента

### Визуальные характеристики

- **Размеры**: 360px × 460px (фиксированные, можно кастомизировать)
- **Цветовая схема**: Черный фон с белыми/серыми акцентами
- **Анимации**:
  - Вращение внешнего бордера (25s)
  - Градиентный фон (20s)
  - Плавающие частицы (5-8s каждая)
  - Fade-in для новых сообщений (0.4s)

---

## Технические требования

### Обязательные зависимости

1. **React** (19.x или выше) - уже установлен ✅
2. **TypeScript** (5.x) - уже установлен ✅
3. **Tailwind CSS** (4.x) - уже установлен ✅
4. **shadcn/ui** - уже настроен ✅
5. **lucide-react** (^0.546.0) - уже установлен ✅
6. **framer-motion** - **требуется установка** ⚠️

### NPM пакеты для установки

```bash
pnpm add framer-motion
```

### Структура проекта

```
frontend/
├── src/
│   ├── components/
│   │   └── ui/
│   │       └── ai-chat.tsx          # <- Компонент чата
│   ├── lib/
│   │   └── utils.ts                 # <- cn() утилита (уже есть)
│   └── app/
│       └── page.tsx                 # <- Место для демо
```

---

## Код компонента

### ai-chat.tsx

Полный код компонента для размещения в `frontend/src/components/ui/ai-chat.tsx`:

```tsx
"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Send } from "lucide-react";
import { cn } from "@/lib/utils";

export default function AIChatCard({ className }: { className?: string }) {
  const [messages, setMessages] = useState<{ sender: "ai" | "user"; text: string }[]>([
    { sender: "ai", text: "👋 Hello! I'm your AI assistant." },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      setMessages((prev) => [...prev, { sender: "ai", text: "🤖 This is a sample AI response." }]);
      setIsTyping(false);
    }, 1200);
  };

  return (
    <div className={cn("relative w-[360px] h-[460px] rounded-2xl overflow-hidden p-[2px]", className)}>
      {/* Animated Outer Border */}
      <motion.div
        className="absolute inset-0 rounded-2xl border-2 border-white/20"
        animate={{ rotate: [0, 360] }}
        transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
      />

      {/* Inner Card */}
      <div className="relative flex flex-col w-full h-full rounded-xl border border-white/10 overflow-hidden bg-black/90 backdrop-blur-xl">
        {/* Inner Animated Background */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-gray-800 via-black to-gray-900"
          animate={{ backgroundPosition: ["0% 0%", "100% 100%", "0% 0%"] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          style={{ backgroundSize: "200% 200%" }}
        />

        {/* Floating Particles */}
        {Array.from({ length: 20 }).map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 rounded-full bg-white/10"
            animate={{
              y: ["0%", "-140%"],
              x: [Math.random() * 200 - 100, Math.random() * 200 - 100],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: 5 + Math.random() * 3,
              repeat: Infinity,
              delay: i * 0.5,
              ease: "easeInOut",
            }}
            style={{ left: `${Math.random() * 100}%`, bottom: "-10%" }}
          />
        ))}

        {/* Header */}
        <div className="px-4 py-3 border-b border-white/10 relative z-10">
          <h2 className="text-lg font-semibold text-white">🤖 AI Assistant</h2>
        </div>

        {/* Messages */}
        <div className="flex-1 px-4 py-3 overflow-y-auto space-y-3 text-sm flex flex-col relative z-10">
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              className={cn(
                "px-3 py-2 rounded-xl max-w-[80%] shadow-md backdrop-blur-md",
                msg.sender === "ai"
                  ? "bg-white/10 text-white self-start"
                  : "bg-white/30 text-black font-semibold self-end"
              )}
            >
              {msg.text}
            </motion.div>
          ))}

          {/* AI Typing Indicator */}
          {isTyping && (
            <motion.div
              className="flex items-center gap-1 px-3 py-2 rounded-xl max-w-[30%] bg-white/10 self-start"
              initial={{ opacity: 0 }}
              animate={{ opacity: [0, 1, 0.6, 1] }}
              transition={{ repeat: Infinity, duration: 1.2 }}
            >
              <span className="w-2 h-2 rounded-full bg-white animate-pulse"></span>
              <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-200"></span>
              <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-400"></span>
            </motion.div>
          )}
        </div>

        {/* Input */}
        <div className="flex items-center gap-2 p-3 border-t border-white/10 relative z-10">
          <input
            className="flex-1 px-3 py-2 text-sm bg-black/50 rounded-lg border border-white/10 text-white focus:outline-none focus:ring-1 focus:ring-white/50"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={handleSend}
            className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
          >
            <Send className="w-4 h-4 text-white" />
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## Демо использования

### Пример интеграции

Простой пример использования компонента:

```tsx
import AIChatCard from "@/components/ui/ai-chat";

export default function DemoPage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-950">
      <AIChatCard />
    </div>
  );
}
```

### С кастомными стилями

```tsx
import AIChatCard from "@/components/ui/ai-chat";

export default function DashboardWithChat() {
  return (
    <div className="p-8">
      <h1>Dashboard</h1>
      <AIChatCard className="mx-auto mt-8" />
    </div>
  );
}
```

---

## Архитектура компонента

### Props

```typescript
interface AIChatCardProps {
  className?: string;  // Дополнительные CSS классы
}
```

### State

```typescript
// Массив сообщений
const [messages, setMessages] = useState<{
  sender: "ai" | "user";
  text: string;
}[]>([...]);

// Текущий ввод пользователя
const [input, setInput] = useState("");

// Индикатор "AI печатает"
const [isTyping, setIsTyping] = useState(false);
```

### Основные функции

**`handleSend()`** - Обработка отправки сообщения:
1. Валидация ввода (не пустое сообщение)
2. Добавление сообщения пользователя в историю
3. Очистка поля ввода
4. Установка статуса "typing"
5. Симуляция ответа AI через 1.2s
6. Добавление ответа AI в историю

---

## Интеграция в проект

### Шаг 1: Установка зависимостей

```bash
cd frontend
pnpm add framer-motion
```

### Шаг 2: Создание компонента

Скопировать код из секции "Код компонента" в файл:
```
frontend/src/components/ui/ai-chat.tsx
```

### Шаг 3: Проверка утилит

Убедиться что `cn()` утилита существует в `src/lib/utils.ts`:

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### Шаг 4: Использование

Импортировать и использовать в любом компоненте/странице:

```tsx
import AIChatCard from "@/components/ui/ai-chat";
```

---

## Адаптация для проекта

### Текущая реализация vs Финальная цель

**Текущая реализация (референс)**:
- Статичные сообщения
- Симуляция ответов с задержкой
- Нет реального API взаимодействия

**Цель для Спринта F4**:
- Интеграция с backend API для чата
- Реальные запросы к LLM через `/api/chat` endpoint
- Поддержка text-to-SQL запросов
- История диалога с контекстом
- Обработка ошибок и edge cases

### Необходимые модификации

1. **API интеграция**:
   - Заменить `setTimeout()` симуляцию на реальный fetch
   - Создать API client для чата (по аналогии с `lib/api.ts`)
   - Добавить обработку ошибок

2. **Расширение State**:
   - Добавить `loading` состояние
   - Добавить `error` состояние
   - Сохранение истории в localStorage (опционально)

3. **Улучшение UX**:
   - Автоскролл к последнему сообщению
   - Форматирование markdown в ответах AI
   - Отображение SQL запросов и результатов
   - Кнопка "Clear chat"

4. **Локализация**:
   - Перевод текстов на русский язык
   - Изменение placeholder: "Задайте вопрос..."
   - Изменение приветствия AI

---

## Стилизация

### Tailwind классы

Компонент использует следующие ключевые Tailwind утилиты:

- **Layout**: `flex`, `flex-col`, `relative`, `absolute`, `inset-0`
- **Sizing**: `w-[360px]`, `h-[460px]`, `max-w-[80%]`
- **Spacing**: `p-[2px]`, `px-4`, `py-3`, `gap-2`
- **Colors**: `bg-black/90`, `border-white/10`, `text-white`
- **Effects**: `backdrop-blur-xl`, `rounded-2xl`, `shadow-md`
- **Animations**: `animate-pulse`, `transition-colors`

### Кастомизация цветов

Для изменения цветовой схемы:

```tsx
// Текущая тема (темная)
bg-black/90          // Фон карточки
border-white/10      // Бордеры
text-white           // Текст AI

// Пример светлой темы
bg-white/90          // Фон карточки
border-gray-200      // Бордеры
text-gray-900        // Текст AI
```

---

## Performance заметки

### Оптимизации

1. **Мемоизация**: Рассмотреть `useMemo` для списка сообщений при большой истории
2. **Виртуализация**: Использовать виртуальный скролл для >100 сообщений
3. **Анимации**: 20 частиц могут быть ресурсоемкими на слабых устройствах

### Рекомендации

```tsx
// Уменьшить количество частиц для мобильных
const particleCount = isMobile ? 10 : 20;

// Отключить сложные анимации для слабых устройств
const enableAnimations = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

---

## Связанные документы

- [Frontend Roadmap](../frontend-roadmap.md) - Общий план развития frontend
- [Sprint F4 Plan](../../.cursor/plans/) - Детальный план реализации (будет создан)
- [Frontend Vision](../../frontend/doc/front-vision.md) - Техническое видение проекта

---

## Следующие шаги

1. ✅ Установить `framer-motion`
2. ✅ Создать компонент `ai-chat.tsx`
3. ⏳ Создать API endpoint `/api/chat`
4. ⏳ Интегрировать с LLM для text-to-SQL
5. ⏳ Добавить компонент на dashboard
6. ⏳ Тестирование и отладка

---

**Версия**: 1.0
**Автор**: Референс от 21st.dev, адаптирован для проекта
**Последнее обновление**: 2025-10-17
