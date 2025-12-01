import { ArrowDownLeft, ArrowUpRight, Filter, Search } from "lucide-react";

interface HistoryItemProps {
    title: string;
    time: string;
    amount: string;
    type: "in" | "out";
    items: string;
}

export function HistoryPage() {
    return (
        <div className="min-h-screen bg-surface pb-24">
            <header className="bg-surface-card border-b border-border px-4 py-3 sticky top-0 z-10 space-y-3">
                <h1 className="text-lg font-bold text-text-main">History</h1>
                <div className="flex gap-2">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-2.5 text-text-muted w-4 h-4" />
                        <input
                            type="text"
                            placeholder="Search transaction..."
                            className="w-full pl-9 pr-4 py-2 bg-surface border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                        />
                    </div>
                    <button className="p-2 border border-border rounded-lg bg-surface-card text-text-muted" aria-label="Filter history">
                        <Filter size={20} />
                    </button>
                </div>
            </header>

            <main className="p-4 space-y-4">
                <section>
                    <h3 className="text-xs font-bold text-text-muted uppercase tracking-wider mb-2 ml-1">Today</h3>
                    <div className="bg-surface-card border border-border rounded-lg overflow-hidden divide-y divide-border">
                        <HistoryItem title="Walk-in Sale" time="2:30 PM" amount="+ ₱145.00" type="in" items="2x Coke, 1x Chips" />
                        <HistoryItem title="Supplier Payment" time="11:00 AM" amount="- ₱2,500.00" type="out" items="Restock: Beverages" />
                        <HistoryItem title="Walk-in Sale" time="9:15 AM" amount="+ ₱60.00" type="in" items="Load (Globe)" />
                    </div>
                </section>

                <section>
                    <h3 className="text-xs font-bold text-text-muted uppercase tracking-wider mb-2 ml-1">Yesterday</h3>
                    <div className="bg-surface-card border border-border rounded-lg overflow-hidden divide-y divide-border">
                        <HistoryItem title="EOD Batch Total" time="9:00 PM" amount="+ ₱12,450.00" type="in" items="Daily Aggregated Sales" />
                    </div>
                </section>
            </main>
        </div>
    );
}

function HistoryItem({ title, time, amount, type, items }: HistoryItemProps) {
    const isIn = type === "in";
    return (
        <div className="p-4 flex justify-between items-start">
            <div className="flex gap-3">
                <div className={`mt-1 p-1.5 rounded-full ${isIn ? "bg-green-100 text-green-700" : "bg-slate-100 text-slate-600"}`}>
                    {isIn ? <ArrowDownLeft size={16} /> : <ArrowUpRight size={16} />}
                </div>
                <div>
                    <div className="text-sm font-bold text-text-main">{title}</div>
                    <div className="text-xs text-text-muted">{items}</div>
                    <div className="text-[10px] text-text-muted mt-1">{time}</div>
                </div>
            </div>
            <div className="text-sm font-bold text-text-main">{amount}</div>
        </div>
    );
}
