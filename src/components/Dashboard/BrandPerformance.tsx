import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { TrendingUp } from "lucide-react";

const brandData = [
  { name: "Coca-Cola", revenue: 15420, share: 28, trend: 5.2, color: "hsl(var(--chart-1))" },
  { name: "San Miguel", revenue: 12350, share: 22, trend: 3.1, color: "hsl(var(--chart-2))" },
  { name: "Nestle", revenue: 10890, share: 19, trend: -1.5, color: "hsl(var(--chart-3))" },
  { name: "Unilever", revenue: 8640, share: 15, trend: 2.8, color: "hsl(var(--chart-4))" },
  { name: "Del Monte", revenue: 7200, share: 13, trend: 4.3, color: "hsl(var(--chart-5))" },
];

export const BrandPerformance = () => {
  return (
    <Card className="p-6 border border-border">
      <div className="mb-6">
        <h3 className="text-lg font-semibold font-heading">Top Brands</h3>
        <p className="text-sm text-muted-foreground">Revenue contribution by brand</p>
      </div>
      <div className="space-y-6">
        {brandData.map((brand) => (
          <div key={brand.name} className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div 
                  className="w-3 h-3 rounded-full" 
                  style={{ backgroundColor: brand.color }}
                />
                <span className="font-medium">{brand.name}</span>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm font-semibold">₱{brand.revenue.toLocaleString()}</span>
                <div className={`flex items-center gap-1 ${brand.trend > 0 ? 'text-success' : 'text-destructive'}`}>
                  <TrendingUp className={`w-3 h-3 ${brand.trend < 0 ? 'rotate-180' : ''}`} />
                  <span className="text-xs font-medium">{Math.abs(brand.trend)}%</span>
                </div>
              </div>
            </div>
            <Progress value={brand.share} className="h-2" />
          </div>
        ))}
      </div>
    </Card>
  );
};
