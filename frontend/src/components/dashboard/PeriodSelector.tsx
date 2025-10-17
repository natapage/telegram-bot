/**
 * Компонент для выбора периода статистики
 */

'use client';

import { Button } from '@/components/ui/button';
import type { Period } from '@/lib/types';

interface PeriodSelectorProps {
    /** Текущий выбранный период */
    period: Period;
    /** Callback при изменении периода */
    onPeriodChange: (period: Period) => void;
}

const PERIOD_LABELS: Record<Period, string> = {
    day: 'День',
    week: 'Неделя',
    month: 'Месяц',
};

/**
 * PeriodSelector - компонент для переключения между периодами (день/неделя/месяц)
 */
export function PeriodSelector({ period, onPeriodChange }: PeriodSelectorProps) {
    const periods: Period[] = ['day', 'week', 'month'];

    return (
        <div className="mb-6 flex gap-2">
            {periods.map((p) => (
                <Button
                    key={p}
                    variant={period === p ? 'default' : 'outline'}
                    onClick={() => onPeriodChange(p)}
                    className="min-w-[100px]"
                >
                    {PERIOD_LABELS[p]}
                </Button>
            ))}
        </div>
    );
}
