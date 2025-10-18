/**
 * Компонент для отображения общей статистики
 */

'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { OverallStats as OverallStatsType } from '@/lib/types';
import { formatNumber, formatDecimal } from '@/lib/format';

interface OverallStatsProps {
    /** Данные общей статистики */
    stats: OverallStatsType;
}

/**
 * OverallStats - отображает 3 карточки с ключевыми метриками
 */
export function OverallStats({ stats }: OverallStatsProps) {
    const metrics = [
        {
            title: 'Всего диалогов',
            value: formatNumber(stats.total_dialogs),
            description: 'уникальных диалогов',
        },
        {
            title: 'Активных пользователей',
            value: formatNumber(stats.active_users),
            description: 'пользователей активны',
        },
        {
            title: 'Средняя длина диалога',
            value: formatDecimal(stats.avg_dialog_length, 1),
            description: 'сообщений на диалог',
        },
    ];

    return (
        <div className="mb-6 grid gap-4 md:grid-cols-3">
            {metrics.map((metric) => (
                <Card key={metric.title}>
                    <CardHeader>
                        <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metric.value}</div>
                        <p className="text-muted-foreground mt-1 text-xs">{metric.description}</p>
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}
