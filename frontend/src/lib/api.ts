/**
 * API Client для взаимодействия с backend
 *
 * Предоставляет типизированные функции для работы с API endpoints
 */

import { API_BASE_URL, API_ENDPOINTS, API_TIMEOUT } from '@/config/api.config';
import type { StatsResponse, HealthResponse, Period, ApiError } from './types';

/**
 * Базовая функция для выполнения fetch запросов с обработкой ошибок
 */
async function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeout: number = API_TIMEOUT
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timeout');
    }
    throw error;
  }
}

/**
 * Обработка ответа от API
 * @throws {ApiError} если ответ не успешный
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ApiError = {
      message: `API request failed: ${response.statusText}`,
      status: response.status,
    };

    try {
      const errorData = await response.json();
      error.message = errorData.message || error.message;
    } catch {
      // Если не удалось распарсить JSON, используем дефолтное сообщение
    }

    throw error;
  }

  return response.json() as Promise<T>;
}

/**
 * API Client объект с методами для каждого endpoint
 */
export const apiClient = {
  /**
   * Health check - проверка работоспособности API
   * @returns Promise с статусом API
   * @example
   * ```ts
   * const health = await apiClient.healthCheck();
   * console.log(health.status); // "ok"
   * ```
   */
  async healthCheck(): Promise<HealthResponse> {
    const url = `${API_BASE_URL}${API_ENDPOINTS.health}`;
    const response = await fetchWithTimeout(url);
    return handleResponse<HealthResponse>(response);
  },

  /**
   * Получение статистики по диалогам за указанный период
   * @param period - период для фильтрации ('day' | 'week' | 'month')
   * @returns Promise с данными статистики
   * @example
   * ```ts
   * const stats = await apiClient.getStats('day');
   * console.log(stats.overall.total_dialogs);
   * ```
   */
  async getStats(period: Period): Promise<StatsResponse> {
    const url = `${API_BASE_URL}${API_ENDPOINTS.stats}?period=${period}`;
    const response = await fetchWithTimeout(url);
    return handleResponse<StatsResponse>(response);
  },
};

/**
 * Функция для проверки доступности API
 * Используется для быстрой проверки соединения
 */
export async function checkApiAvailability(): Promise<boolean> {
  try {
    await apiClient.healthCheck();
    return true;
  } catch {
    return false;
  }
}
