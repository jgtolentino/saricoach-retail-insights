import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Lightbulb, TrendingUp, Package, Users, ArrowRight } from "lucide-react";

const recommendations = [
  {
    id: 1,
    priority: "high",
    icon: TrendingUp,
    title: "Stock up on best-sellers",
    description: "Your top 5 products are selling 40% faster than usual. Consider increasing inventory to avoid stockouts this weekend.",
    impact: "Potential ₱8,500 additional revenue",
    action: "View suggested orders",
  },
  {
    id: 2,
    priority: "medium",
    icon: Package,
    title: "Slow-moving inventory alert",
    description: "You have ₱12,300 worth of products that haven't sold in 3 weeks. Consider promotional bundles or discounts.",
    impact: "Free up shelf space & capital",
    action: "See products",
  },
  {
    id: 3,
    priority: "medium",
    icon: Users,
    title: "Peak hours optimization",
    description: "Transaction data shows 60% of sales happen between 4-7 PM. Ensure adequate staffing during these hours.",
    impact: "Reduce wait times by 35%",
    action: "View schedule",
  },
];

const priorityColors = {
  high: "bg-destructive/10 text-destructive border-destructive/20",
  medium: "bg-warning/10 text-warning border-warning/20",
  low: "bg-primary/10 text-primary border-primary/20",
};

export const AIRecommendations = () => {
  return (
    <Card className="p-6 border border-border">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-primary/10">
          <Lightbulb className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h3 className="text-lg font-semibold font-heading">AI Coach Recommendations</h3>
          <p className="text-sm text-muted-foreground">Personalized insights to grow your business</p>
        </div>
      </div>
      <div className="space-y-4">
        {recommendations.map((rec) => {
          const Icon = rec.icon;
          return (
            <div 
              key={rec.id}
              className="p-4 rounded-lg border border-border bg-muted/30 hover:bg-muted/50 transition-smooth"
            >
              <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-primary/10 mt-1">
                  <Icon className="w-4 h-4 text-primary" />
                </div>
                <div className="flex-1 space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <h4 className="font-semibold text-sm">{rec.title}</h4>
                    <Badge 
                      variant="outline" 
                      className={priorityColors[rec.priority as keyof typeof priorityColors]}
                    >
                      {rec.priority}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{rec.description}</p>
                  <div className="flex items-center justify-between pt-2">
                    <span className="text-xs font-medium text-success">{rec.impact}</span>
                    <Button variant="ghost" size="sm" className="gap-1 h-8">
                      {rec.action}
                      <ArrowRight className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
