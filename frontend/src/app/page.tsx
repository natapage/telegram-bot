'use client';

import { useStats } from '@/hooks/useStats';
import { PeriodSelector } from '@/components/dashboard/PeriodSelector';
import { OverallStats } from '@/components/dashboard/OverallStats';
import { ActivityChart } from '@/components/dashboard/ActivityChart';
import { RecentDialogs } from '@/components/dashboard/RecentDialogs';
import { TopUsers } from '@/components/dashboard/TopUsers';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertCircle, Loader2, Github } from 'lucide-react';
import { GITHUB_REPO_URL } from '@/config/api.config';

/**
 * Loading State компонент
 */
function LoadingState() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <Card key={i}>
            <CardContent className="bg-muted h-24 animate-pulse p-6" />
          </Card>
        ))}
      </div>
      <Card>
        <CardContent className="flex h-[400px] items-center justify-center">
          <Loader2 className="text-muted-foreground h-12 w-12 animate-spin" />
        </CardContent>
      </Card>
      <div className="grid gap-6 md:grid-cols-2">
        {[1, 2].map((i) => (
          <Card key={i}>
            <CardContent className="bg-muted h-[300px] animate-pulse p-6" />
          </Card>
        ))}
      </div>
    </div>
  );
}

/**
 * Error State компонент
 */
function ErrorState({ error, onRetry }: { error: string; onRetry: () => void }) {
  return (
    <Card className="p-8 text-center">
      <AlertCircle className="text-destructive mx-auto h-12 w-12" />
      <h3 className="mt-4 text-lg font-semibold">Ошибка загрузки данных</h3>
      <p className="text-muted-foreground mt-2">{error}</p>
      <Button onClick={onRetry} className="mt-4">
        Повторить попытку
      </Button>
    </Card>
  );
}

/**
 * Empty State компонент
 */
function EmptyState() {
  return (
    <Card className="p-8 text-center">
      <h3 className="text-lg font-semibold">Нет данных</h3>
      <p className="text-muted-foreground mt-2">
        Статистика пока недоступна. Начните использовать бота, чтобы увидеть данные здесь.
      </p>
    </Card>
  );
}

/**
 * Dashboard - главная страница с визуализацией статистики
 */
export default function Dashboard() {
  const { data, loading, error, period, setPeriod, retry } = useStats('day');

  return (
    <div className="bg-background min-h-screen p-4 md:p-8">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <header className="mb-8 flex items-start justify-between">
          <div>
            <h1 className="text-4xl font-bold">Telegram Bot Dashboard</h1>
            <p className="text-muted-foreground mt-2">
              Статистика и аналитика диалогов с пользователями
            </p>
          </div>
          <a
            href={GITHUB_REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="transition-opacity hover:opacity-80"
          >
            <Button variant="outline" className="gap-2">
              <Github className="h-5 w-5" />
              <span>GitHub</span>
            </Button>
          </a>
        </header>

        {/* Period Selector */}
        <PeriodSelector period={period} onPeriodChange={setPeriod} />

        {/* Loading State */}
        {loading && <LoadingState />}

        {/* Error State */}
        {error && !loading && <ErrorState error={error} onRetry={retry} />}

        {/* Empty State */}
        {!loading && !error && data && data.overall.total_dialogs === 0 && <EmptyState />}

        {/* Data Display */}
        {!loading && !error && data && data.overall.total_dialogs > 0 && (
          <>
            {/* Overall Stats */}
            <OverallStats stats={data.overall} />

            {/* Activity Chart */}
            <ActivityChart data={data.activity_data} period={period} />

            {/* Recent Dialogs and Top Users */}
            <div className="grid gap-6 md:grid-cols-2">
              <RecentDialogs dialogs={data.recent_dialogs} />
              <TopUsers users={data.top_users} />
            </div>
          </>
        )}

        {/* Footer */}
        <footer className="text-muted-foreground mt-12 text-center text-sm">
          <p>Sprint F3 - Dashboard реализован ✅</p>
          <p className="mt-2">
            Backend API: <code className="bg-muted rounded px-2 py-1">http://localhost:8000</code>
          </p>
        </footer>
      </div>
    </div>
  );
}
