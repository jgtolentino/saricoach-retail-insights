import { Card } from "@/components/ui/card";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const data = [
  { date: "Mon", revenue: 2400, transactions: 45 },
  { date: "Tue", revenue: 1800, transactions: 38 },
  { date: "Wed", revenue: 3200, transactions: 52 },
  { date: "Thu", revenue: 2800, transactions: 48 },
  { date: "Fri", revenue: 4100, transactions: 68 },
  { date: "Sat", revenue: 5200, transactions: 82 },
  { date: "Sun", revenue: 4500, transactions: 71 },
];

export const RevenueChart = () => {
  return (
    <Card className="p-6 border border-border">
      <div className="mb-6">
        <h3 className="text-lg font-semibold font-heading">Revenue Trend</h3>
        <p className="text-sm text-muted-foreground">Daily revenue over the past week</p>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis 
            dataKey="date" 
            stroke="hsl(var(--muted-foreground))"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke="hsl(var(--muted-foreground))"
            style={{ fontSize: '12px' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'hsl(var(--card))',
              border: '1px solid hsl(var(--border))',
              borderRadius: '8px',
            }}
          />
          <Area
            type="monotone"
            dataKey="revenue"
            stroke="hsl(var(--primary))"
            strokeWidth={2}
            fill="url(#colorRevenue)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </Card>
  );
};
