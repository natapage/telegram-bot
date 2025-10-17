/**
 * Компонент для отображения последних диалогов
 */

'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import type { RecentDialog } from '@/lib/types';
import { formatDate, truncateText, formatNumber } from '@/lib/format';

interface RecentDialogsProps {
    /** Список последних диалогов */
    dialogs: RecentDialog[];
}

/**
 * RecentDialogs - таблица последних 10 диалогов
 */
export function RecentDialogs({ dialogs }: RecentDialogsProps) {
    if (dialogs.length === 0) {
        return (
            <Card>
                <CardHeader>
                    <CardTitle>Последние диалоги</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground text-center text-sm">Нет данных о диалогах</p>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Последние диалоги</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="overflow-x-auto">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>User ID</TableHead>
                                <TableHead className="hidden md:table-cell">Последнее сообщение</TableHead>
                                <TableHead className="hidden lg:table-cell">Дата создания</TableHead>
                                <TableHead className="text-right">Сообщений</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {dialogs.map((dialog) => (
                                <TableRow key={dialog.user_id}>
                                    <TableCell className="font-medium">{dialog.user_id}</TableCell>
                                    <TableCell className="hidden md:table-cell">
                                        <span className="text-muted-foreground text-sm">
                                            {truncateText(dialog.last_message, 60)}
                                        </span>
                                    </TableCell>
                                    <TableCell className="text-muted-foreground hidden text-sm lg:table-cell">
                                        {formatDate(dialog.created_at)}
                                    </TableCell>
                                    <TableCell className="text-right">{formatNumber(dialog.message_count)}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>

                {/* Mobile view - показываем информацию по-другому */}
                <div className="space-y-3 md:hidden">
                    {dialogs.map((dialog) => (
                        <div key={dialog.user_id} className="border-b pb-3 last:border-0">
                            <div className="mb-1 flex items-center justify-between">
                                <span className="font-medium">User #{dialog.user_id}</span>
                                <span className="text-muted-foreground text-sm">
                                    {formatNumber(dialog.message_count)} сообщений
                                </span>
                            </div>
                            <p className="text-muted-foreground text-sm">
                                {truncateText(dialog.last_message, 100)}
                            </p>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
