/**
 * Тесты для useStats hook
 */

import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useStats } from '../useStats';
import { apiClient } from '@/lib/api';
import type { StatsResponse } from '@/lib/types';

// Mock API client
vi.mock('@/lib/api', () => ({
    apiClient: {
        getStats: vi.fn(),
    },
}));

const mockStatsResponse: StatsResponse = {
    overall: {
        total_dialogs: 100,
        active_users: 75,
        avg_dialog_length: 12.5,
    },
    activity_data: [
        { timestamp: '2025-10-17T10:00:00Z', message_count: 50 },
        { timestamp: '2025-10-17T11:00:00Z', message_count: 75 },
    ],
    recent_dialogs: [],
    top_users: [],
    period: 'day',
};

describe('useStats', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should load data on mount', async () => {
        vi.mocked(apiClient.getStats).mockResolvedValue(mockStatsResponse);

        const { result } = renderHook(() => useStats('day'));

        expect(result.current.loading).toBe(true);
        expect(result.current.data).toBeNull();

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.data).toEqual(mockStatsResponse);
        expect(result.current.error).toBeNull();
        expect(apiClient.getStats).toHaveBeenCalledWith('day');
    });

    it('should reload data when period changes', async () => {
        vi.mocked(apiClient.getStats).mockResolvedValue(mockStatsResponse);

        const { result } = renderHook(() => useStats('day'));

        await waitFor(() => expect(result.current.loading).toBe(false));

        // Change period
        result.current.setPeriod('week');

        await waitFor(() => {
            expect(apiClient.getStats).toHaveBeenCalledWith('week');
        });

        expect(result.current.period).toBe('week');
    });

    it('should handle API errors', async () => {
        const errorMessage = 'Network error';
        vi.mocked(apiClient.getStats).mockRejectedValue(new Error(errorMessage));

        const { result } = renderHook(() => useStats('day'));

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.error).toBe(errorMessage);
        expect(result.current.data).toBeNull();
    });

    it('should retry loading on retry call', async () => {
        vi.mocked(apiClient.getStats)
            .mockRejectedValueOnce(new Error('Failed'))
            .mockResolvedValueOnce(mockStatsResponse);

        const { result } = renderHook(() => useStats('day'));

        await waitFor(() => {
            expect(result.current.error).toBe('Failed');
        });

        // Retry
        result.current.retry();

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
            expect(result.current.data).toEqual(mockStatsResponse);
            expect(result.current.error).toBeNull();
        });
    });
});
