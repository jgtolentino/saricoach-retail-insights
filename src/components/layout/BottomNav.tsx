import React from 'react';
import { Home, BarChart3, LineChart, Settings } from 'lucide-react';

interface NavButtonProps {
    icon: React.ReactNode;
    label: string;
    isActive: boolean;
    onClick: () => void;
}

const NavButton: React.FC<NavButtonProps> = ({ icon, label, isActive, onClick }) => (
    <button
        onClick={onClick}
        className={`flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors duration-200 ${isActive ? 'text-blue-600' : 'text-gray-500'}`}
    >
        {icon}
        <span className="text-[10px] font-medium">{label}</span>
    </button>
);

interface BottomNavProps {
    tab: string;
    onChange: (tab: any) => void;
}

export const BottomNav: React.FC<BottomNavProps> = ({ tab, onChange }) => {
    return (
        <nav className="h-16 bg-white border-t border-gray-200 flex items-center justify-around px-2 pb-safe">
            <NavButton
                icon={<Home size={24} />}
                label="Home"
                isActive={tab === 'home'}
                onClick={() => onChange('home')}
            />
            <NavButton
                icon={<BarChart3 size={24} />}
                label="Insights"
                isActive={tab === 'insights'}
                onClick={() => onChange('insights')}
            />
            <NavButton
                icon={<LineChart size={24} />}
                label="History"
                isActive={tab === 'history'}
                onClick={() => onChange('history')}
            />
            <NavButton
                icon={<Settings size={24} />}
                label="Settings"
                isActive={tab === 'settings'}
                onClick={() => onChange('settings')}
            />
        </nav>
    );
};
