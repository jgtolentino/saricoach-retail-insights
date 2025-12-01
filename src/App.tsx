import { useState } from 'react';
import { HomePage } from './pages/HomePage';
import { BottomNav } from './components/layout/BottomNav';
import { CoachChat } from './components/coach/CoachChat';

// Placeholder pages for now
const InsightsPage = () => <div className="p-4">Insights Page Placeholder</div>;
const HistoryPage = () => <div className="p-4">History Page Placeholder</div>;
const SettingsPage = () => <div className="p-4">Settings Page Placeholder</div>;

function App() {
    const [activeTab, setActiveTab] = useState<'home' | 'insights' | 'history' | 'settings'>('home');

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            <main className="flex-1 overflow-y-auto">
                {activeTab === 'home' && <HomePage />}
                {activeTab === 'insights' && <InsightsPage />}
                {activeTab === 'history' && <HistoryPage />}
                {activeTab === 'settings' && <SettingsPage />}
            </main>
            <BottomNav tab={activeTab} onChange={setActiveTab} />
            <CoachChat />
        </div>
    );
}

export default App;
