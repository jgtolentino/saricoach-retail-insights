import React from 'react';

interface MetricCardProps {
    label: string;
    value: string | number;
    trend?: 'up' | 'down' | 'neutral';
    trendValue?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({ label, value, trend, trendValue }) => {
    // Logic to determine status color token
    const trendColor = trend === 'up' ? 'text-status-success' :
        trend === 'down' ? 'text-status-error' : 'text-text-muted';
    const Arrow = trend === 'up' ? '▲' : trend === 'down' ? '▼' : '•';

    return (
        <div className="bg-surface-card border border-border rounded-lg p-4 shadow-sm flex flex-col justify-between h-28">
            {/* Label using Muted Token */}
            <span className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                {label}
            </span>

            <div>
                {/* Value using Main Text Token */}
                <div className="text-2xl font-bold text-text-main tracking-tight">
                    {value}
                </div>

                {/* Trend using Status Token */}
                {trendValue && (
                    <div className={`text-xs font-medium mt-1 flex items-center gap-1 ${trendColor}`}>
                        <span>{Arrow}</span>
                        <span>{trendValue}</span>
                    </div>
                )}
            </div>
        </div>
    );
};
