/**
 * Тесты для OverallStats компонента
 */

import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { OverallStats } from '../OverallStats';
import type { OverallStats as OverallStatsType } from '@/lib/types';

describe('OverallStats', () => {
    const mockStats: OverallStatsType = {
        total_dialogs: 145,
        active_users: 89,
        avg_dialog_length: 12.3,
    };

    it('should render all three metrics', () => {
        render(<OverallStats stats={mockStats} />);

        expect(screen.getByText('Всего диалогов')).toBeInTheDocument();
        expect(screen.getByText('Активных пользователей')).toBeInTheDocument();
        expect(screen.getByText('Средняя длина диалога')).toBeInTheDocument();
    });

    it('should format numbers correctly', () => {
        render(<OverallStats stats={mockStats} />);

        expect(screen.getByText('145')).toBeInTheDocument();
        expect(screen.getByText('89')).toBeInTheDocument();
        expect(screen.getByText('12.3')).toBeInTheDocument();
    });

    it('should format large numbers with thousands separator', () => {
        const largeStats: OverallStatsType = {
            total_dialogs: 1234,
            active_users: 5678,
            avg_dialog_length: 10.5,
        };

        render(<OverallStats stats={largeStats} />);

        // Russian locale uses non-breaking space as separator
        expect(screen.getByText(/1\s?234/)).toBeInTheDocument();
        expect(screen.getByText(/5\s?678/)).toBeInTheDocument();
    });
});
