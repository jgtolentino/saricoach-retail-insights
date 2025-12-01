import React, { useState } from 'react';
import { HomePage } from './pages/Home';
import { Home, BarChart3, LineChart, Settings } from 'lucide-react';

import { InsightsPage } from './pages/Insights';
import { HistoryPage } from './pages/History';
import { SettingsPage } from './pages/Settings';
import { ChatAssistant } from './components/ChatAssistant';
import SupabaseDebug from './pages/SupabaseDebug';

function App() {
    const [activeTab, setActiveTab] = useState<'home' | 'insights' | 'history' | 'settings' | 'debug'>('home');

    const renderContent = () => {
        switch (activeTab) {
            case 'home': return <HomePage />;
            case 'insights': return <InsightsPage />;
            case 'history': return <HistoryPage />;
            case 'settings': return <SettingsPage />;
            case 'debug': return <SupabaseDebug />;
        }
    };

    return (
        <div className="min-h-screen bg-[var(--color-background)] flex flex-col font-sans relative">
            <div className="flex-1 overflow-hidden flex flex-col">
                {renderContent()}
            </div>

            {/* AI Chat Assistant */}
            <ChatAssistant />

            {/* Bottom Navigation */}
            <nav className="h-16 bg-[var(--color-surface)] border-t border-[var(--color-outline)] flex items-center justify-around px-2 pb-safe">
                <NavButton
                    icon={<Home size={24} />}
                    label="Home"
                    isActive={activeTab === 'home'}
                    onClick={() => setActiveTab('home')}
                />
                <NavButton
                    icon={<BarChart3 size={24} />}
                    label="Insights"
                    isActive={activeTab === 'insights'}
                    onClick={() => setActiveTab('insights')}
                />
                <NavButton
                    icon={<LineChart size={24} />}
                    label="History"
                    isActive={activeTab === 'history'}
                    onClick={() => setActiveTab('history')}
                />
                <NavButton
                    icon={<Settings size={24} />}
                    label="Settings"
                    isActive={activeTab === 'settings'}
                    onClick={() => setActiveTab('settings')}
                />
            </nav>
        </div>
    );
}

interface NavButtonProps {
    icon: React.ReactNode;
    label: string;
    isActive: boolean;
    onClick: () => void;
}

const NavButton: React.FC<NavButtonProps> = ({ icon, label, isActive, onClick }) => (
    <button
        onClick={onClick}
        className={`flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors duration-200 ${isActive ? 'text-[var(--color-primary)]' : 'text-[var(--color-text-secondary)]'
            }`}
    >
        {icon}
        <span className="text-[10px] font-medium">{label}</span>
    </button>
);

export default App;
