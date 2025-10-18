/**
 * Тесты для RecentDialogs компонента
 */

import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { RecentDialogs } from '../RecentDialogs';
import type { RecentDialog } from '@/lib/types';

describe('RecentDialogs', () => {
    const mockDialogs: RecentDialog[] = [
        {
            user_id: 123456789,
            last_message: 'Спасибо за помощь!',
            created_at: '2025-10-17T18:45:23Z',
            message_count: 15,
        },
        {
            user_id: 987654321,
            last_message: 'Можешь посоветовать что-то для расслабления?',
            created_at: '2025-10-17T17:32:10Z',
            message_count: 8,
        },
    ];

    it('should render dialog list', () => {
        render(<RecentDialogs dialogs={mockDialogs} />);

        expect(screen.getByText('Последние диалоги')).toBeInTheDocument();
        expect(screen.getByText('123456789')).toBeInTheDocument();
        expect(screen.getByText('987654321')).toBeInTheDocument();
    });

    it('should show empty state when no dialogs', () => {
        render(<RecentDialogs dialogs={[]} />);

        expect(screen.getByText('Нет данных о диалогах')).toBeInTheDocument();
    });

    it('should truncate long messages', () => {
        const longDialog: RecentDialog = {
            user_id: 111222333,
            last_message: 'A'.repeat(100),
            created_at: '2025-10-17T10:00:00Z',
            message_count: 5,
        };

        render(<RecentDialogs dialogs={[longDialog]} />);

        const messageElements = screen.getAllByText(/A+/);
        // Should be truncated to 60 chars + "..."
        messageElements.forEach((element) => {
            expect(element.textContent!.length).toBeLessThanOrEqual(63);
        });
    });
});
