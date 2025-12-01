// dashboard/src/pages/History.tsx
import React from 'react';

export const HistoryPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-[var(--color-background)] flex flex-col">
            <header className="pt-4 px-4 pb-2">
                <div className="text-xl font-semibold text-[var(--color-text-primary)]">
                    History
                </div>
            </header>
            <main className="flex-1 px-4 pb-4 flex items-center justify-center text-[var(--color-text-secondary)]">
                <div className="text-center">
                    <p>Historical trends coming soon.</p>
                    <p className="text-xs mt-2">Will show sales vs weather/traffic correlations.</p>
                </div>
            </main>
        </div>
    );
};
