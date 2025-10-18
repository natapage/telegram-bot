/**
 * Тесты для PeriodSelector компонента
 */

import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import { PeriodSelector } from '../PeriodSelector';

describe('PeriodSelector', () => {
    it('should render all period buttons', () => {
        const onPeriodChange = vi.fn();
        render(<PeriodSelector period="day" onPeriodChange={onPeriodChange} />);

        expect(screen.getByText('День')).toBeInTheDocument();
        expect(screen.getByText('Неделя')).toBeInTheDocument();
        expect(screen.getByText('Месяц')).toBeInTheDocument();
    });

    it('should highlight active period', () => {
        const onPeriodChange = vi.fn();
        render(<PeriodSelector period="week" onPeriodChange={onPeriodChange} />);

        const weekButton = screen.getByText('Неделя');
        expect(weekButton).toHaveClass('bg-primary'); // default variant имеет bg-primary
    });

    it('should call onPeriodChange when button clicked', async () => {
        const onPeriodChange = vi.fn();
        const user = userEvent.setup();

        render(<PeriodSelector period="day" onPeriodChange={onPeriodChange} />);

        const weekButton = screen.getByText('Неделя');
        await user.click(weekButton);

        expect(onPeriodChange).toHaveBeenCalledWith('week');
    });
});
