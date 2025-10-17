import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function Dashboard() {
  return (
    <div className="bg-background min-h-screen p-8">
      {/* Header */}
      <header className="mb-8">
        <h1 className="text-4xl font-bold">Telegram Bot Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Статистика и аналитика диалогов с пользователями
        </p>
      </header>

      {/* Period Selector Placeholder */}
      <div className="mb-6">
        <div className="flex gap-2">
          <Button variant="default">День</Button>
          <Button variant="outline">Неделя</Button>
          <Button variant="outline">Месяц</Button>
        </div>
      </div>

      {/* Dashboard Grid */}
      <div className="grid gap-6">
        {/* Overall Stats Section */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Всего диалогов</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">52</div>
              <p className="text-muted-foreground text-xs">за последние 24 часа</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Активных пользователей</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">41</div>
              <p className="text-muted-foreground text-xs">уникальных пользователей</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Средняя длина диалога</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">11.5</div>
              <p className="text-muted-foreground text-xs">сообщений на диалог</p>
            </CardContent>
          </Card>
        </div>

        {/* Activity Chart Section */}
        <Card>
          <CardHeader>
            <CardTitle>График активности</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex h-[300px] items-center justify-center rounded-lg border-2 border-dashed">
              <p className="text-muted-foreground">Activity Chart будет здесь (Спринт F3)</p>
            </div>
          </CardContent>
        </Card>

        {/* Recent Dialogs and Top Users */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Recent Dialogs */}
          <Card>
            <CardHeader>
              <CardTitle>Последние диалоги</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="border-b pb-3">
                  <p className="font-medium">User #123456789</p>
                  <p className="text-muted-foreground text-sm">Спасибо за помощь!</p>
                  <p className="text-muted-foreground mt-1 text-xs">15 сообщений</p>
                </div>
                <div className="border-b pb-3">
                  <p className="font-medium">User #987654321</p>
                  <p className="text-muted-foreground text-sm">Как настроить параметры?</p>
                  <p className="text-muted-foreground mt-1 text-xs">8 сообщений</p>
                </div>
                <p className="text-muted-foreground pt-2 text-center text-sm">
                  Полный список в Спринте F3
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Top Users */}
          <Card>
            <CardHeader>
              <CardTitle>Топ пользователей</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b pb-3">
                  <div>
                    <p className="font-medium">User #111222333</p>
                    <p className="text-muted-foreground text-xs">
                      Последняя активность: 2 часа назад
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold">95</p>
                    <p className="text-muted-foreground text-xs">сообщений</p>
                  </div>
                </div>
                <div className="flex items-center justify-between border-b pb-3">
                  <div>
                    <p className="font-medium">User #444555666</p>
                    <p className="text-muted-foreground text-xs">
                      Последняя активность: 5 часов назад
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold">78</p>
                    <p className="text-muted-foreground text-xs">сообщений</p>
                  </div>
                </div>
                <p className="text-muted-foreground pt-2 text-center text-sm">
                  Полный топ в Спринте F3
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Footer */}
      <footer className="text-muted-foreground mt-12 text-center text-sm">
        <p>Sprint F2 - Frontend инициализация завершена ✅</p>
        <p className="mt-2">
          Backend API: <code className="bg-muted rounded px-2 py-1">http://localhost:8000</code>
        </p>
      </footer>
    </div>
  );
}
