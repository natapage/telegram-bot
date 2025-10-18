/**
 * Custom hook для загрузки статистики диалогов
 * Управляет состоянием загрузки, ошибок и данных
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/lib/api';
import type { StatsResponse, Period } from '@/lib/types';

interface UseStatsReturn {
    /** Данные статистики */
    data: StatsResponse | null;
    /** Состояние загрузки */
    loading: boolean;
    /** Сообщение об ошибке */
    error: string | null;
    /** Текущий выбранный период */
    period: Period;
    /** Функция для изменения периода */
    setPeriod: (period: Period) => void;
    /** Функция для повторной попытки загрузки */
    retry: () => void;
}

/**
 * Hook для получения статистики диалогов с автоматической перезагрузкой
 * @param initialPeriod - начальный период (по умолчанию 'day')
 * @returns объект с данными, состояниями и функциями управления
 */
export function useStats(initialPeriod: Period = 'day'): UseStatsReturn {
    const [period, setPeriod] = useState<Period>(initialPeriod);
    const [data, setData] = useState<StatsResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [retryTrigger, setRetryTrigger] = useState(0);

    const retry = useCallback(() => {
        setRetryTrigger((prev) => prev + 1);
    }, []);

    useEffect(() => {
        let mounted = true;

        async function fetchStats() {
            try {
                setLoading(true);
                setError(null);

                const response = await apiClient.getStats(period);

                if (mounted) {
                    setData(response);
                }
            } catch (err) {
                if (mounted) {
                    const errorMessage =
                        err instanceof Error ? err.message : 'Не удалось загрузить статистику';
                    setError(errorMessage);
                    console.error('Error fetching stats:', err);
                }
            } finally {
                if (mounted) {
                    setLoading(false);
                }
            }
        }

        fetchStats();

        return () => {
            mounted = false;
        };
    }, [period, retryTrigger]);

    return {
        data,
        loading,
        error,
        period,
        setPeriod,
        retry,
    };
}
