import { Header } from "@/components/Layout/Header";
import { Sidebar } from "@/components/Layout/Sidebar";
import { MetricCard } from "@/components/Dashboard/MetricCard";
import { RevenueChart } from "@/components/Dashboard/RevenueChart";
import { BrandPerformance } from "@/components/Dashboard/BrandPerformance";
import { AIRecommendations } from "@/components/Dashboard/AIRecommendations";
import { RecentTransactions } from "@/components/Dashboard/RecentTransactions";
import { DollarSign, ShoppingCart, TrendingUp, Package } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <Sidebar />
      
      <main className="ml-64 pt-16">
        <div className="container py-8">
          <div className="mb-8">
            <h2 className="text-3xl font-bold font-heading mb-2">Welcome back! 👋</h2>
            <p className="text-muted-foreground">Here's what's happening with your store today</p>
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 animate-slide-up">
            <MetricCard
              title="Total Revenue"
              value="₱54,240"
              change={12.5}
              trend="up"
              icon={DollarSign}
              iconColor="text-primary"
              description="Last 7 days"
            />
            <MetricCard
              title="Transactions"
              value="348"
              change={8.2}
              trend="up"
              icon={ShoppingCart}
              iconColor="text-accent"
              description="Avg. ₱156 per transaction"
            />
            <MetricCard
              title="Daily Average"
              value="₱7,749"
              change={-3.1}
              trend="down"
              icon={TrendingUp}
              iconColor="text-success"
              description="Revenue per day"
            />
            <MetricCard
              title="Stock Value"
              value="₱89,320"
              change={5.7}
              trend="up"
              icon={Package}
              iconColor="text-chart-4"
              description="Current inventory"
            />
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div className="lg:col-span-2">
              <RevenueChart />
            </div>
            <div className="lg:col-span-1">
              <BrandPerformance />
            </div>
          </div>

          {/* Bottom Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AIRecommendations />
            <RecentTransactions />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
