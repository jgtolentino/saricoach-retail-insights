// dashboard/src/components/KpiCard.tsx
import React from "react";

interface KpiCardProps {
    label: string;
    value: string;
    subtitle?: string;
}

export const KpiCard: React.FC<KpiCardProps> = ({ label, value, subtitle }) => {
    return (
        <div className="min-w-[140px] bg-[var(--color-surface)] rounded-[var(--radius-card)] px-4 py-3 mr-3 shadow-sm border border-[var(--color-outline)]">
            <div className="text-xs text-[var(--color-text-secondary)] mb-1">{label}</div>
            <div className="text-lg font-semibold text-[var(--color-text-primary)]">{value}</div>
            {subtitle && (
                <div className="text-[10px] text-[var(--color-text-secondary)] mt-1">
                    {subtitle}
                </div>
            )}
        </div>
    );
};
