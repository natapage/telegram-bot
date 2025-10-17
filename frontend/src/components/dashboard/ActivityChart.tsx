/**
 * Компонент для отображения графика активности
 */

'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { format, parseISO } from 'date-fns';
import { ru } from 'date-fns/locale';
import type { ActivityDataPoint, Period } from '@/lib/types';

interface ActivityChartProps {
    /** Данные для графика активности */
    data: ActivityDataPoint[];
    /** Период для адаптации оси X */
    period: Period;
}

/**
 * Форматирует метку оси X в зависимости от периода
 */
function formatXAxis(timestamp: string, period: Period): string {
    const date = parseISO(timestamp);

    switch (period) {
        case 'day':
            // Для дня: часы (0-23)
            return format(date, 'HH:mm', { locale: ru });
        case 'week':
            // Для недели: дни недели (Пн-Вс)
            return format(date, 'EEE', { locale: ru });
        case 'month':
            // Для месяца: даты (1-30)
            return format(date, 'd MMM', { locale: ru });
        default:
            return format(date, 'HH:mm', { locale: ru });
    }
}

/**
 * ActivityChart - график активности пользователей во времени
 */
export function ActivityChart({ data, period }: ActivityChartProps) {
    // Преобразуем данные для Recharts
    const chartData = data.map((point) => ({
        timestamp: point.timestamp,
        count: point.message_count,
        label: formatXAxis(point.timestamp, period),
    }));

    return (
        <Card className="mb-6">
            <CardHeader>
                <CardTitle>График активности</CardTitle>
            </CardHeader>
            <CardContent>
                <ResponsiveContainer width="100%" height={350}>
                    <AreaChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <defs>
                            <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" opacity={0.3} />
                        <XAxis
                            dataKey="label"
                            className="text-xs"
                            tick={{ fill: 'hsl(var(--muted-foreground))' }}
                            axisLine={{ stroke: 'hsl(var(--border))' }}
                            tickLine={{ stroke: 'hsl(var(--border))' }}
                        />
                        <YAxis
                            className="text-xs"
                            tick={{ fill: 'hsl(var(--muted-foreground))' }}
                            axisLine={{ stroke: 'hsl(var(--border))' }}
                            tickLine={{ stroke: 'hsl(var(--border))' }}
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'hsl(var(--background))',
                                border: '1px solid hsl(var(--border))',
                                borderRadius: '8px',
                                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
                            }}
                            labelStyle={{ color: 'hsl(var(--foreground))', fontWeight: 600 }}
                            formatter={(value: number) => [`${value} сообщений`, 'Активность']}
                        />
                        <Area
                            type="monotone"
                            dataKey="count"
                            stroke="hsl(var(--primary))"
                            strokeWidth={2}
                            fill="url(#colorCount)"
                            dot={false}
                            activeDot={{
                                r: 6,
                                fill: 'hsl(var(--primary))',
                                stroke: 'hsl(var(--background))',
                                strokeWidth: 2,
                            }}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
}
