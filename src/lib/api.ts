const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchStoreSummary(storeId: number) {
    try {
        const res = await fetch(`${API_URL}/api/store/${storeId}/summary`);
        if (!res.ok) throw new Error("Failed to load store summary");
        return await res.json();
    } catch (error) {
        console.error(error);
        throw error;
    }
}
