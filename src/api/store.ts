// dashboard/src/api/store.ts

import { apiGet } from "./client";

export interface CoachResponse {
    actions: string[];
    risks: string[];
    opportunities: string[];
    debug_notes: Record<string, unknown>;
}

export interface StoreSummaryResponse {
    store_id: number;
    date: string;
    kpis: {
        daily_sales: number;
        daily_sales_delta: number;
        stockout_risk: string;
        hot_brand: string | null;
    };
    coach: CoachResponse;
}

export function getStoreSummary(storeId: number) {
    return apiGet<StoreSummaryResponse>(`/api/store/${storeId}/summary`);
}
