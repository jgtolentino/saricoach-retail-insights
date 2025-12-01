import type { ComponentType } from "react";
import { Bell, ChevronRight, Database, LogOut, Store, User } from "lucide-react";

interface SectionHeaderProps {
    label: string;
}

interface SettingsRowProps {
    icon: ComponentType<{ size?: number; className?: string }>;
    label: string;
    value?: string;
    color?: string;
}

interface ToggleRowProps {
    label: string;
    description: string;
}

export function SettingsPage() {
    return (
        <div className="min-h-screen bg-surface pb-24">
            <header className="bg-surface-card border-b border-border px-4 py-4 sticky top-0 z-10">
                <h1 className="text-lg font-bold text-text-main">Settings</h1>
            </header>

            <main className="p-4 space-y-6">
                <div className="flex items-center gap-4 bg-surface-card p-4 rounded-lg border border-border shadow-sm">
                    <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold text-xl">S</div>
                    <div>
                        <h2 className="text-base font-bold text-text-main">Sari-Sari Store #1</h2>
                        <p className="text-xs text-text-muted">Owner: Maria Cruz</p>
                    </div>
                </div>

                <div className="space-y-2">
                    <SectionHeader label="Store Configuration" />
                    <div className="bg-surface-card rounded-lg border border-border divide-y divide-border overflow-hidden">
                        <SettingsRow icon={Store} label="Store Profile" />
                        <SettingsRow icon={Bell} label="Notifications" value="On" />
                        <SettingsRow icon={User} label="Staff Accounts" />
                    </div>
                </div>

                <div className="space-y-2">
                    <SectionHeader label="Data &amp; Intelligence" />
                    <div className="bg-surface-card rounded-lg border border-border divide-y divide-border overflow-hidden">
                        <SettingsRow icon={Database} label="Data Source" value="Supabase (Live)" color="text-status-success" />
                        <ToggleRow label="Enable Shelf Vision" description="Use camera to track stock" />
                        <ToggleRow label="Daily Coach Briefing" description="Receive AI summary at 8 AM" />
                    </div>
                </div>

                <button className="w-full flex items-center justify-center gap-2 text-status-error font-medium p-4 bg-surface-card border border-border rounded-lg">
                    <LogOut size={18} />
                    Sign Out
                </button>

                <div className="text-center text-xs text-text-muted pt-4">SariCoach v1.0.2 (Build 2025.12)</div>
            </main>
        </div>
    );
}

function SectionHeader({ label }: SectionHeaderProps) {
    return <h3 className="text-xs font-bold text-text-muted uppercase tracking-wider ml-1">{label}</h3>;
}

function SettingsRow({ icon: Icon, label, value, color }: SettingsRowProps) {
    return (
        <button className="w-full px-4 py-3.5 flex items-center justify-between hover:bg-surface transition-colors">
            <div className="flex items-center gap-3">
                <Icon size={18} className="text-text-muted" />
                <span className="text-sm text-text-main font-medium">{label}</span>
            </div>
            <div className="flex items-center gap-2">
                {value && <span className={`text-sm ${color || "text-text-muted"}`}>{value}</span>}
                <ChevronRight size={16} className="text-text-muted" />
            </div>
        </button>
    );
}

function ToggleRow({ label, description }: ToggleRowProps) {
    return (
        <div className="px-4 py-3.5 flex items-center justify-between">
            <div>
                <div className="text-sm text-text-main font-medium">{label}</div>
                <div className="text-xs text-text-muted">{description}</div>
            </div>
            <div className="w-10 h-6 bg-primary rounded-full relative cursor-pointer" aria-label={`${label} toggle`}>
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm" />
            </div>
        </div>
    );
}
