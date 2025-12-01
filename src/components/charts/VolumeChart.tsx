import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

// Define the shape of data this chart expects
interface ChartData {
    date: string; // "08:00", "10:00", etc.
    volume: number;
}

interface VolumeChartProps {
    data: ChartData[];
}

export const VolumeChart = ({ data }: VolumeChartProps) => {
    // If no data, show a clean empty state
    if (!data || data.length === 0) {
        return (
            <div className="h-40 w-full flex items-center justify-center text-text-muted text-xs bg-surface rounded-lg">
                No traffic data available
            </div>
        );
    }

    return (
        <div className="h-48 w-full -ml-4"> {/* Negative margin to let chart bleed to edges slightly */}
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                    <defs>
                        {/* Gradient Definition: Fades from Blue to Transparent */}
                        <linearGradient id="colorVolume" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#2563EB" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
                        </linearGradient>
                    </defs>

                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />

                    <XAxis
                        dataKey="date"
                        axisLine={false}
                        tickLine={false}
                        tick={{ fontSize: 10, fill: '#64748B' }} // text-text-muted
                        tickMargin={10}
                    />

                    <YAxis
                        hide={true} // Hide Y Axis numbers to keep it clean on mobile
                    />

                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#FFFFFF',
                            borderRadius: '8px',
                            border: '1px solid #E2E8F0',
                            fontSize: '12px',
                            boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
                        }}
                        itemStyle={{ color: '#0F172A', fontWeight: 'bold' }}
                        cursor={{ stroke: '#2563EB', strokeWidth: 1, strokeDasharray: '4 4' }}
                    />

                    <Area
                        type="monotone"
                        dataKey="volume"
                        stroke="#2563EB" // primary color
                        strokeWidth={2}
                        fillOpacity={1}
                        fill="url(#colorVolume)"
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};
