import React from 'react';

interface KpiCardProps {
    label: string;
    value: string | number;
    deltaPct?: number;
    trend?: 'up' | 'down' | 'neutral';
}

export const KpiCard: React.FC<KpiCardProps> = ({ label, value, deltaPct, trend }) => {
    const isPositive = deltaPct && deltaPct > 0;
    const colorClass = isPositive ? 'text-green-600' : 'text-red-600';
    const arrow = isPositive ? '▲' : '▼';

    return (
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col">
            <span className="text-xs text-gray-500 font-medium uppercase tracking-wider">{label}</span>
            <div className="mt-1 flex items-end justify-between">
                <span className="text-2xl font-bold text-gray-900">{value}</span>
                {deltaPct && (
                    <span className={`text-xs font-bold ${colorClass} bg-gray-50 px-1.5 py-0.5 rounded`}>
                        {arrow} {Math.abs(deltaPct)}%
                    </span>
                )}
            </div>
        </div>
    );
};
