/**
 * Конфигурация API endpoints и настроек
 *
 * Использует environment variables для гибкой настройки
 */

/**
 * Базовый URL backend API
 * Берется из переменной окружения NEXT_PUBLIC_API_URL
 * По умолчанию: http://localhost:8000 (Mock API)
 */
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * API endpoints
 */
export const API_ENDPOINTS = {
  /** Health check endpoint */
  health: '/health',
  /** Статистика по диалогам с параметром period */
  stats: '/stats',
} as const;

/**
 * Таймаут для API запросов (в миллисекундах)
 */
export const API_TIMEOUT = 10000; // 10 секунд

/**
 * Retry настройки для failed requests
 */
export const API_RETRY_CONFIG = {
  /** Максимальное количество повторных попыток */
  maxRetries: 3,
  /** Задержка между попытками (в миллисекундах) */
  retryDelay: 1000,
} as const;

/**
 * GitHub repository URL
 * Берется из переменной окружения NEXT_PUBLIC_GITHUB_REPO_URL
 */
export const GITHUB_REPO_URL =
  process.env.NEXT_PUBLIC_GITHUB_REPO_URL || 'https://github.com/yourusername/telegram-bot';
