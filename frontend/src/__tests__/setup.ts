/**
 * Vitest глобальные настройки и setup
 * Выполняется перед запуском всех тестов
 */

import { vi } from 'vitest';
import '@testing-library/jest-dom';

// Мокаем environment variables для тестов
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';

// Мокаем fetch API если нужно
// eslint-disable-next-line @typescript-eslint/no-explicit-any
global.fetch = vi.fn() as any;

// Дополнительные глобальные настройки можно добавить здесь
