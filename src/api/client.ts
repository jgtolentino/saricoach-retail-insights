// dashboard/src/api/client.ts
export const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function apiGet<T>(path: string): Promise<T> {
    const res = await fetch(`${API_BASE_URL}${path}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json() as Promise<T>;
}
