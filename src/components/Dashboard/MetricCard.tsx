import { LucideIcon } from "lucide-react";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon: LucideIcon;
  description?: string;
  trend?: "up" | "down" | "neutral";
  iconColor?: string;
}

export const MetricCard = ({
  title,
  value,
  change,
  icon: Icon,
  description,
  trend = "neutral",
  iconColor = "text-primary",
}: MetricCardProps) => {
  const trendColors = {
    up: "text-success",
    down: "text-destructive",
    neutral: "text-muted-foreground",
  };

  return (
    <Card className="metric-card">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-muted-foreground mb-1">{title}</p>
          <p className="stat-number text-foreground">{value}</p>
          {change !== undefined && (
            <div className="flex items-center gap-1 mt-2">
              <span className={cn("text-sm font-medium", trendColors[trend])}>
                {change > 0 ? "+" : ""}
                {change}%
              </span>
              <span className="text-xs text-muted-foreground">vs last period</span>
            </div>
          )}
          {description && (
            <p className="text-xs text-muted-foreground mt-1">{description}</p>
          )}
        </div>
        <div className={cn("p-3 rounded-xl bg-muted/50", iconColor)}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </Card>
  );
};
