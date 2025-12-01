import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock } from "lucide-react";

const transactions = [
  { id: "TXN-2847", time: "2 mins ago", items: 5, amount: 485, status: "completed" },
  { id: "TXN-2846", time: "8 mins ago", items: 3, amount: 320, status: "completed" },
  { id: "TXN-2845", time: "15 mins ago", items: 7, amount: 640, status: "completed" },
  { id: "TXN-2844", time: "23 mins ago", items: 2, amount: 180, status: "completed" },
  { id: "TXN-2843", time: "31 mins ago", items: 4, amount: 420, status: "completed" },
];

export const RecentTransactions = () => {
  return (
    <Card className="p-6 border border-border">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold font-heading">Recent Transactions</h3>
          <p className="text-sm text-muted-foreground">Latest sales activity</p>
        </div>
        <Badge variant="secondary" className="gap-1">
          <Clock className="w-3 h-3" />
          Live
        </Badge>
      </div>
      <div className="space-y-3">
        {transactions.map((tx) => (
          <div 
            key={tx.id}
            className="flex items-center justify-between p-3 rounded-lg border border-border hover:bg-muted/50 transition-smooth"
          >
            <div className="flex items-center gap-3">
              <div className="flex flex-col">
                <span className="font-mono text-sm font-medium">{tx.id}</span>
                <span className="text-xs text-muted-foreground">{tx.time}</span>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <div className="text-sm font-medium">{tx.items} items</div>
                <div className="text-xs text-muted-foreground">₱{tx.amount}</div>
              </div>
              <Badge variant="outline" className="bg-success/10 text-success border-success/20">
                {tx.status}
              </Badge>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
