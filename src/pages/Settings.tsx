// dashboard/src/pages/Settings.tsx
import React from 'react';

export const SettingsPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-[var(--color-background)] flex flex-col">
            <header className="pt-4 px-4 pb-2">
                <div className="text-xl font-semibold text-[var(--color-text-primary)]">
                    Settings
                </div>
            </header>
            <main className="flex-1 px-4 pb-4">
                <div className="bg-[var(--color-surface)] rounded-2xl p-4 mb-4">
                    <h3 className="text-sm font-semibold mb-2">Store Profile</h3>
                    <div className="text-sm text-[var(--color-text-secondary)]">
                        <p>Store ID: 1</p>
                        <p>Name: Sari Sari ni Aling Maria</p>
                    </div>
                </div>

                <div className="bg-[var(--color-surface)] rounded-2xl p-4">
                    <h3 className="text-sm font-semibold mb-2">Data Sources</h3>
                    <div className="space-y-2 text-sm">
                        <div className="flex items-center justify-between">
                            <span>Sales Data</span>
                            <span className="text-[var(--color-success)]">Active</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span>Shelf Vision</span>
                            <span className="text-[var(--color-success)]">Active</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span>Weather & Traffic</span>
                            <span className="text-[var(--color-success)]">Active</span>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};
