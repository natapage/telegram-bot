/**
 * Тесты для TopUsers компонента
 */

import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { TopUsers } from '../TopUsers';
import type { TopUser } from '@/lib/types';

describe('TopUsers', () => {
    const mockUsers: TopUser[] = [
        {
            user_id: 333444555,
            message_count: 20,
            last_active: '2025-10-17T10:50:12Z',
        },
        {
            user_id: 444555666,
            message_count: 18,
            last_active: '2025-10-17T14:05:18Z',
        },
        {
            user_id: 123456789,
            message_count: 15,
            last_active: '2025-10-17T18:45:23Z',
        },
    ];

    it('should render user list', () => {
        render(<TopUsers users={mockUsers} />);

        expect(screen.getByText('Топ пользователей')).toBeInTheDocument();
        expect(screen.getByText('User #333444555')).toBeInTheDocument();
        expect(screen.getByText('User #444555666')).toBeInTheDocument();
        expect(screen.getByText('User #123456789')).toBeInTheDocument();
    });

    it('should show position badges', () => {
        render(<TopUsers users={mockUsers} />);

        expect(screen.getByText('1')).toBeInTheDocument();
        expect(screen.getByText('2')).toBeInTheDocument();
        expect(screen.getByText('3')).toBeInTheDocument();
    });

    it('should show empty state when no users', () => {
        render(<TopUsers users={[]} />);

        expect(screen.getByText('Нет данных о пользователях')).toBeInTheDocument();
    });

    it('should display message counts', () => {
        render(<TopUsers users={mockUsers} />);

        expect(screen.getByText('20')).toBeInTheDocument();
        expect(screen.getByText('18')).toBeInTheDocument();
        expect(screen.getByText('15')).toBeInTheDocument();
    });
});
