// dashboard/src/pages/Home.tsx
import React, { useEffect, useState } from "react";
import { getStoreSummary, StoreSummaryResponse } from "../api/store";
import { KpiCard } from "../components/KpiCard";
import { CoachPanel } from "../components/CoachPanel";

const DEFAULT_STORE_ID = 1;

export const HomePage: React.FC = () => {
    const [data, setData] = useState<StoreSummaryResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [err, setErr] = useState<string | null>(null);

    useEffect(() => {
        setLoading(true);
        getStoreSummary(DEFAULT_STORE_ID)
            .then((res) => {
                setData(res);
                setErr(null);
            })
            .catch((e) => {
                console.error(e);
                setErr("Failed to load store summary");
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return <div className="p-4 text-sm text-[var(--color-text-secondary)]">Loading…</div>;
    }

    if (err || !data) {
        return <div className="p-4 text-sm text-red-500">{err ?? "No data"}</div>;
    }

    const { kpis, coach } = data;
    const deltaPct = (kpis.daily_sales_delta * 100).toFixed(1);

    return (
        <div className="min-h-screen bg-[var(--color-background)] flex flex-col">
            <header className="pt-4 px-4 pb-2">
                <div className="text-xs text-[var(--color-text-secondary)]">
                    Today · Store #{data.store_id}
                </div>
                <div className="text-xl font-semibold text-[var(--color-text-primary)]">
                    SariCoach
                </div>
            </header>

            <main className="flex-1 px-4 pb-4 overflow-y-auto">
                {/* KPI row */}
                <div className="flex overflow-x-auto pb-2 -ml-4 pl-4">
                    <KpiCard
                        label="Daily Sales"
                        value={`₱${kpis.daily_sales.toLocaleString()}`}
                        subtitle={`${deltaPct}% vs yesterday`}
                    />
                    <KpiCard
                        label="Stockout Risk"
                        value={kpis.stockout_risk ?? "—"}
                    />
                    <KpiCard
                        label="Hot Brand"
                        value={kpis.hot_brand ?? "–"}
                    />
                </div>

                {/* Coach panel */}
                <CoachPanel coach={coach} />

                {/* Risks & opportunities (simple list for now) */}
                <section className="mb-4">
                    <h2 className="text-sm font-semibold text-[var(--color-text-primary)] mb-1">
                        Risks
                    </h2>
                    <ul className="list-disc pl-5 space-y-1 text-xs text-[var(--color-text-primary)]">
                        {coach.risks.slice(0, 3).map((r, idx) => (
                            <li key={idx}>{r}</li>
                        ))}
                    </ul>
                </section>

                <section>
                    <h2 className="text-sm font-semibold text-[var(--color-text-primary)] mb-1">
                        Opportunities
                    </h2>
                    <ul className="list-disc pl-5 space-y-1 text-xs text-[var(--color-text-primary)]">
                        {coach.opportunities.slice(0, 3).map((o, idx) => (
                            <li key={idx}>{o}</li>
                        ))}
                    </ul>
                </section>
            </main>

        </div>
    );
};
