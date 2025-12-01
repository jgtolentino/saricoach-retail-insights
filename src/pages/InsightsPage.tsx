import { ArrowDownRight, ArrowUpRight, Package, TrendingUp } from "lucide-react";
import { VolumeChart } from "../components/charts/VolumeChart";

const WEEKLY_DATA = [
    { date: "Mon", volume: 4500 },
    { date: "Tue", volume: 3200 },
    { date: "Wed", volume: 5100 },
    { date: "Thu", volume: 4800 },
    { date: "Fri", volume: 6900 },
    { date: "Sat", volume: 8200 },
    { date: "Sun", volume: 7100 }
];

type TrendDirection = "up" | "down";

interface ListItemProps {
    name: string;
    metric: string;
    subtext: string;
    trend: TrendDirection;
}

interface CategoryBarProps {
    label: string;
    percent: number;
    color: string;
}

export function InsightsPage() {
    return (
        <div className="min-h-screen bg-surface pb-24">
            <header className="bg-surface-card border-b border-border px-4 py-4 sticky top-0 z-10">
                <h1 className="text-lg font-bold text-text-main">Weekly Insights</h1>
                <p className="text-xs text-text-muted">Nov 25 - Dec 02</p>
            </header>

            <main className="p-4 space-y-4">
                <div className="bg-surface-card border border-border rounded-lg p-4 shadow-sm">
                    <div className="flex justify-between items-center mb-4">
                        <div>
                            <h3 className="text-sm font-bold text-text-main">Revenue Trend</h3>
                            <div className="flex items-center gap-1 text-xs text-status-success font-medium mt-0.5">
                                <TrendingUp size={14} />
                                <span>+12.5% vs last week</span>
                            </div>
                        </div>
                        <span className="text-2xl font-bold text-text-main">₱39.8k</span>
                    </div>
                    <VolumeChart data={WEEKLY_DATA} />
                </div>

                <div className="bg-surface-card border border-border rounded-lg shadow-sm overflow-hidden">
                    <div className="px-4 py-3 border-b border-border">
                        <h3 className="text-sm font-bold text-text-main">Top Movers</h3>
                    </div>

                    <div className="divide-y divide-border">
                        <ListItem name="Coke 1.5L" metric="₱1,200" subtext="48 units sold" trend="up" />
                        <ListItem name="Bear Brand Swak" metric="₱850" subtext="92 units sold" trend="up" />
                        <ListItem name="Marlboro Red" metric="₱4,100" subtext="Volume down 5%" trend="down" />
                    </div>
                </div>

                <div className="bg-surface-card border border-border rounded-lg p-4 shadow-sm">
                    <h3 className="text-sm font-bold text-text-main mb-3">Sales by Category</h3>
                    <div className="space-y-3">
                        <CategoryBar label="Beverages" percent={45} color="bg-blue-500" />
                        <CategoryBar label="Cigarettes" percent={30} color="bg-indigo-500" />
                        <CategoryBar label="Canned Goods" percent={15} color="bg-sky-400" />
                        <CategoryBar label="Load / Data" percent={10} color="bg-slate-300" />
                    </div>
                </div>
            </main>
        </div>
    );
}

function ListItem({ name, metric, subtext, trend }: ListItemProps) {
    const isUp = trend === "up";
    return (
        <div className="px-4 py-3 flex justify-between items-center">
            <div className="flex items-center gap-3">
                <div className="bg-surface p-2 rounded-md text-primary">
                    <Package size={18} />
                </div>
                <div>
                    <div className="text-sm font-bold text-text-main">{name}</div>
                    <div className="text-xs text-text-muted">{subtext}</div>
                </div>
            </div>
            <div className="text-right">
                <div className="text-sm font-bold text-text-main">{metric}</div>
                {isUp ? (
                    <div className="text-[10px] text-status-success flex items-center justify-end gap-0.5">
                        <ArrowUpRight size={12} /> High Demand
                    </div>
                ) : (
                    <div className="text-[10px] text-status-error flex items-center justify-end gap-0.5">
                        <ArrowDownRight size={12} /> Low Stock
                    </div>
                )}
            </div>
        </div>
    );
}

function CategoryBar({ label, percent, color }: CategoryBarProps) {
    return (
        <div>
            <div className="flex justify-between text-xs mb-1">
                <span className="text-text-body font-medium">{label}</span>
                <span className="text-text-muted">{percent}%</span>
            </div>
            <div className="h-2 w-full bg-surface rounded-full overflow-hidden">
                <div className={`h-full ${color}`} style={{ width: `${percent}%` }} />
            </div>
        </div>
    );
}
