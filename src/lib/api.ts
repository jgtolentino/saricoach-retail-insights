// We use a relative path. Vercel will see "/api" and forward it to DigitalOcean.
const API_URL = "";

export async function fetchStoreSummary(storeId: number) {
    console.log("Fetching from:", `${API_URL}/api/store/${storeId}/summary`); // Debug log

    const res = await fetch(`${API_URL}/api/store/${storeId}/summary`);

    // 1. Check if the response is actually JSON
    const contentType = res.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
        const text = await res.text();
        console.error("Received HTML instead of JSON:", text.slice(0, 100)); // Log the HTML
        throw new Error("API configuration error: Backend returned HTML. Check VITE_API_URL.");
    }

    // 2. Handle API errors
    if (!res.ok) {
        throw new Error(`API Error: ${res.status}`);
    }

    return res.json();
}
