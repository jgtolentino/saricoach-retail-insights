import { cn } from "@/lib/utils";
import { 
  LayoutDashboard, 
  Package, 
  TrendingUp, 
  Users, 
  FileText, 
  Sparkles,
  Settings,
  HelpCircle
} from "lucide-react";

const navigation = [
  { name: "Dashboard", icon: LayoutDashboard, href: "/", active: true },
  { name: "Inventory", icon: Package, href: "/inventory" },
  { name: "Analytics", icon: TrendingUp, href: "/analytics" },
  { name: "Customers", icon: Users, href: "/customers" },
  { name: "Reports", icon: FileText, href: "/reports" },
  { name: "AI Insights", icon: Sparkles, href: "/insights" },
];

const secondaryNav = [
  { name: "Settings", icon: Settings, href: "/settings" },
  { name: "Help & Support", icon: HelpCircle, href: "/help" },
];

export const Sidebar = () => {
  return (
    <aside className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 border-r border-border bg-card">
      <nav className="flex flex-col h-full p-4">
        <div className="flex-1 space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <a
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-smooth",
                  item.active
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                <Icon className="w-5 h-5" />
                {item.name}
              </a>
            );
          })}
        </div>
        
        <div className="border-t border-border pt-4 space-y-1">
          {secondaryNav.map((item) => {
            const Icon = item.icon;
            return (
              <a
                key={item.name}
                href={item.href}
                className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-smooth"
              >
                <Icon className="w-5 h-5" />
                {item.name}
              </a>
            );
          })}
        </div>
      </nav>
    </aside>
  );
};
