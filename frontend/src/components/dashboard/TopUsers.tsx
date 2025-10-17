/**
 * Компонент для отображения топ пользователей
 */

'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { TopUser } from '@/lib/types';
import { formatRelativeTime, formatNumber } from '@/lib/format';

interface TopUsersProps {
    /** Список топ пользователей */
    users: TopUser[];
}

/**
 * TopUsers - список топ 5 самых активных пользователей
 */
export function TopUsers({ users }: TopUsersProps) {
    if (users.length === 0) {
        return (
            <Card>
                <CardHeader>
                    <CardTitle>Топ пользователей</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground text-center text-sm">Нет данных о пользователях</p>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Топ пользователей</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    {users.map((user, index) => (
                        <div
                            key={user.user_id}
                            className="flex items-center justify-between border-b pb-3 last:border-0"
                        >
                            <div className="flex items-center gap-3">
                                {/* Номер места */}
                                <div className="bg-primary text-primary-foreground flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold">
                                    {index + 1}
                                </div>
                                <div>
                                    <p className="font-medium">User #{user.user_id}</p>
                                    <p className="text-muted-foreground text-xs">
                                        {formatRelativeTime(user.last_active)}
                                    </p>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="font-bold">{formatNumber(user.message_count)}</p>
                                <p className="text-muted-foreground text-xs">сообщений</p>
                            </div>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
