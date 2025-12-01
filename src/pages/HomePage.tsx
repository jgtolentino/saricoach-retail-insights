import { Settings } from 'lucide-react';
import { MetricCard } from '../components/cards/MetricCard';
import { InsightCard } from '../components/cards/InsightCard';
import { VolumeChart } from '../components/charts/VolumeChart';

export function HomePage() {
    // Mock data for now - will connect to Lovable Cloud later
    const data = {
        store_name: "Sari-Sari Store #1",
        period: "Today",
        coach_message: "Welcome to your store dashboard! Connect your data to get personalized insights.",
        kpis: [
            { label: "Revenue", value: "₱0", trend: "neutral" as const },
            { label: "Transactions", value: "0", trend: "neutral" as const },
            { label: "Avg Basket", value: "₱0", trend: "neutral" as const },
            { label: "Top Item", value: "-", trend: "neutral" as const }
        ],
        chart: []
    };

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
