import { useState } from 'react';
import { Send, Sparkles, X } from 'lucide-react';

// Use relative path to leverage Vercel Proxy (fixes Mixed Content)
const API_URL = "";

export function CoachChat() {
    const [isOpen, setIsOpen] = useState(false);
    const [input, setInput] = useState('');
    const [response, setResponse] = useState<string | null>(null);
    const [isThinking, setIsThinking] = useState(false);

    // NEW: Text-to-Speech Function
    const speakResponse = (text: string) => {
        if (!window.speechSynthesis) return;

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);

        // Optional: Select a voice (try to find a female/Google voice)
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.name.includes("Google") || v.name.includes("Female"));
        if (preferredVoice) utterance.voice = preferredVoice;

        utterance.rate = 1.1; // Slightly faster
        utterance.pitch = 1.0;

        window.speechSynthesis.speak(utterance);
    };

    const handleAsk = async () => {
        if (!input.trim()) return;

        setIsThinking(true);
        setResponse(null);

        try {
            const res = await fetch(`${API_URL}/api/coach/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ store_id: 1, question: input }),
            });

            if (!res.ok) throw new Error('Coach is unreachable');

            const data = await res.json();
            setResponse(data.answer);

            // 🗣️ Trigger Speech here!
            speakResponse(data.answer);

        } catch (err) {
            setResponse("Sorry, I'm having trouble connecting to the store data right now.");
        } finally {
            setIsThinking(false);
        }
    };

    // Minimized State (Floating Action Button)
    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-20 right-4 bg-blue-600 text-white p-4 rounded-full shadow-xl z-50 hover:bg-blue-700 transition-all flex items-center gap-2"
            >
                <Sparkles size={24} />
                <span className="font-bold pr-1">Ask Coach</span>
            </button>
        );
    }

    // Expanded State (Chat Card)
    return (
        <div className="fixed bottom-0 left-0 w-full z-50 p-4">
            {/* Backdrop to close */}
            <div className="fixed inset-0 bg-black/20" onClick={() => setIsOpen(false)} />

            <div className="relative bg-white rounded-t-2xl shadow-2xl flex flex-col max-h-[80vh] w-full max-w-md mx-auto overflow-hidden animate-in slide-in-from-bottom-10">

                {/* Header */}
                <div className="p-4 bg-blue-600 text-white flex justify-between items-center">
                    <div className="flex items-center gap-2">
                        <Sparkles size={18} />
                        <h3 className="font-bold">SariCoach AI</h3>
                    </div>
                    <button onClick={() => setIsOpen(false)} className="hover:bg-blue-500 p-1 rounded">
                        <X size={20} />
                    </button>
                </div>

                {/* Response Area */}
                <div className="p-4 bg-gray-50 min-h-[200px] overflow-y-auto">
                    {!response && !isThinking && (
                        <p className="text-gray-500 text-sm text-center mt-10">
                            Ask me about sales, inventory, or strategy based on today's data.
                        </p>
                    )}

                    {isThinking && (
                        <div className="flex items-center gap-2 text-blue-600 text-sm font-medium animate-pulse">
                            <Sparkles size={16} />
                            Analyzing store metrics...
                        </div>
                    )}

                    {response && (
                        <div className="bg-white p-4 rounded-xl border border-blue-100 shadow-sm text-gray-800 text-sm leading-relaxed">
                            {response}
                        </div>
                    )}
                </div>

                {/* Input Area */}
                <div className="p-3 border-t bg-white flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
                        placeholder="e.g., Why is revenue down?"
                        className="flex-1 bg-gray-100 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                        onClick={handleAsk}
                        disabled={isThinking || !input}
                        className="bg-blue-600 text-white p-2 rounded-full disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
}
