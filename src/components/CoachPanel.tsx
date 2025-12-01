// dashboard/src/components/CoachPanel.tsx
import React from "react";
import type { CoachResponse } from "../api/store";

interface CoachPanelProps {
    coach: CoachResponse | null;
}

export const CoachPanel: React.FC<CoachPanelProps> = ({ coach }) => {
    if (!coach) return null;

    return (
        <div
            className="bg-[var(--color-primary-soft)] rounded-[var(--radius-card)] p-4 mb-4"
            style={{ boxShadow: "var(--md-sys-elevation-level1)" }}
        >
            <div className="flex items-center justify-between mb-2">
                <div>
                    <div className="text-xs text-[var(--color-text-secondary)]">Coach Suggestions</div>
                    <div className="text-base font-semibold text-[var(--color-text-primary)]">
                        Next 7 days
                    </div>
                </div>
            </div>

            <ul className="list-disc pl-5 space-y-1 text-sm text-[var(--color-text-primary)]">
                {coach.actions.slice(0, 4).map((a, idx) => (
                    <li key={idx}>{a}</li>
                ))}
            </ul>
        </div>
    );
};
