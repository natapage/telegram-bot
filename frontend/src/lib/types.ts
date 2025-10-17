/**
 * TypeScript типы и интерфейсы для API интеграции
 *
 * Типы соответствуют контракту Mock API из backend
 * @see doc/api-contract-example.json
 */

/**
 * Период для фильтрации статистики
 */
export type Period = 'day' | 'week' | 'month';

/**
 * Общая статистика по диалогам
 */
export interface OverallStats {
  /** Количество уникальных диалогов за период */
  total_dialogs: number;
  /** Количество активных пользователей за период */
  active_users: number;
  /** Средняя длина диалога (количество сообщений) */
  avg_dialog_length: number;
}

/**
 * Точка данных для графика активности
 */
export interface ActivityDataPoint {
  /** Временная метка в ISO 8601 формате */
  timestamp: string;
  /** Количество сообщений в этот период */
  message_count: number;
}

/**
 * Информация о недавнем диалоге
 */
export interface RecentDialog {
  /** ID пользователя Telegram */
  user_id: number;
  /** Превью последнего сообщения (первые 100 символов) */
  last_message: string;
  /** Дата создания диалога в ISO 8601 формате */
  created_at: string;
  /** Количество сообщений в диалоге */
  message_count: number;
}

/**
 * Информация о топ пользователе
 */
export interface TopUser {
  /** ID пользователя Telegram */
  user_id: number;
  /** Количество сообщений за период */
  message_count: number;
  /** Дата последней активности в ISO 8601 формате */
  last_active: string;
}

/**
 * Полный ответ от API endpoint /stats
 */
export interface StatsResponse {
  /** Общая статистика */
  overall: OverallStats;
  /** Данные для графика активности (24/7/30 точек) */
  activity_data: ActivityDataPoint[];
  /** Список последних 10 диалогов */
  recent_dialogs: RecentDialog[];
  /** Топ 5 самых активных пользователей */
  top_users: TopUser[];
  /** Период за который собрана статистика */
  period: Period;
}

/**
 * Ответ от health check endpoint
 */
export interface HealthResponse {
  /** Статус API (обычно "ok") */
  status: string;
}

/**
 * Ошибка API
 */
export interface ApiError {
  /** Сообщение об ошибке */
  message: string;
  /** HTTP статус код */
  status?: number;
}
