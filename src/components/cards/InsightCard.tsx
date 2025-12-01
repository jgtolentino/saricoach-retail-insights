import { Sparkles } from 'lucide-react';

export const InsightCard = ({ message }: { message: string }) => {
    return (
        <div className="bg-primary-subtle border-l-4 border-primary rounded-r-lg p-4 mb-6">
            <div className="flex items-start gap-3">
                <div className="bg-white p-1.5 rounded-full shadow-sm">
                    <Sparkles className="w-4 h-4 text-primary" />
                </div>
                <div>
                    <h4 className="text-sm font-bold text-primary mb-1">Coach Insight</h4>
                    <p className="text-sm text-text-body leading-relaxed">
                        {message}
                    </p>
                </div>
            </div>
        </div>
    );
};
