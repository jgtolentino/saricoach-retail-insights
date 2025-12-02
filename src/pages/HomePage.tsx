import { useEffect, useState } from 'react';
import { Settings } from 'lucide-react';
import { MetricCard } from '../components/cards/MetricCard';
import { InsightCard } from '../components/cards/InsightCard';
import { VolumeChart } from '../components/charts/VolumeChart';

type Kpi = {
    label: string;
    value: string | number;
    delta_pct?: number | null;
    trend?: 'up' | 'down' | 'neutral';
};

type ChartPoint = {
    date: string;
    volume: number;
};

type StoreSummary = {
    store_id: number;
    store_name: string;
    period: string;
    kpis: Kpi[];
    chart: ChartPoint[];
    insights: string[];
    coach_message: string;
};

const DEFAULT_STORE_ID = 1;

export function HomePage() {
    const [data, setData] = useState<StoreSummary | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setLoading(true);
        fetch(`/api/store/${DEFAULT_STORE_ID}/summary`)
            .then(async (res) => {
                if (!res.ok) {
                    throw new Error(`Failed to load store summary (${res.status})`);
                }
                return res.json();
            })
            .then((json: StoreSummary) => {
                setData(json);
                setError(null);
            })
            .catch((err: Error) => {
                console.error(err);
                setError("Failed to load store summary");
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return <div className="p-4 text-sm text-text-muted">Loading store data…</div>;
    }

    if (error || !data) {
        return <div className="p-4 text-sm text-status-error">{error ?? "No data"}</div>;
    }

    return (
        <div className="min-h-screen bg-surface pb-24">
            {/* Header */}
            <header className="bg-surface-card border-b border-border px-4 py-4 sticky top-0 z-10 flex justify-between items-center animate-in slide-in-from-top-4 duration-700">
                <div>
                    <h1 className="text-lg font-bold text-text-main">{data.store_name}</h1>
                    <p className="text-xs text-text-muted">{data.period}</p>
                </div>
                <button className="p-2 hover:bg-surface-hover rounded-full">
                    <Settings className="w-5 h-5 text-text-muted" />
                </button>
            </header>

            <main className="p-4 space-y-6">

                {/* Insight Feed */}
                {/* Insight Feed */}
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 delay-100 fill-mode-backwards">
                    {data.coach_message && (
                        <InsightCard message={data.coach_message} />
                    )}
                </div>

                {/* Metric Grid */}
                <div className="grid grid-cols-2 gap-3 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200 fill-mode-backwards">
                    {data.kpis.map((kpi, idx: number) => (
                        <MetricCard
                            key={idx}
                            label={kpi.label}
                            value={kpi.value}
                            trend={kpi.trend}
                            trendValue={kpi.delta_pct ? `${Math.abs(kpi.delta_pct)}%` : undefined}
                        />
                    ))}
                </div>

                {/* Chart Section */}
                <div className="bg-surface-card border border-border rounded-lg p-4 shadow-sm animate-in fade-in zoom-in-95 duration-1000 delay-300 fill-mode-backwards">
                    <div className="flex justify-between items-center mb-2">
                        <h3 className="text-sm font-bold text-text-main">Hourly Traffic</h3>
                        <span className="text-xs text-primary font-medium">Today</span>
                    </div>

                    {/* Real Chart Component */}
                    <VolumeChart data={data.chart} />

                </div>
            </main>
        </div>
    );
}
