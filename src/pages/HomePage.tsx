import { useEffect, useState } from 'react';
import { fetchStoreSummary } from '../lib/api';
import { MetricCard } from '../components/cards/MetricCard';
import { InsightCard } from '../components/cards/InsightCard';
import { VolumeChart } from '../components/charts/VolumeChart';
import { Settings, Loader2 } from 'lucide-react';

export function HomePage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStoreSummary(1)
            .then((res) => {
                setData(res);
                setLoading(false);
            })
            .catch((err) => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    if (loading) return (
        <div className="h-screen flex items-center justify-center text-primary">
            <Loader2 className="animate-spin w-8 h-8" />
        </div>
    );

    if (!data) return <div className="p-4 text-center">Failed to load data.</div>;

    return (
        <div className="min-h-screen bg-surface pb-24">
            {/* Header */}
            <header className="bg-surface-card border-b border-border px-4 py-4 sticky top-0 z-10 flex justify-between items-center">
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
                {data.coach_message && (
                    <InsightCard message={data.coach_message} />
                )}

                {/* Metric Grid */}
                <div className="grid grid-cols-2 gap-3">
                    {data.kpis.map((kpi: any, idx: number) => (
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
                <div className="bg-surface-card border border-border rounded-lg p-4 shadow-sm">
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
