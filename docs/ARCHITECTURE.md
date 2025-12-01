# System Architecture & Deployment Strategy 🏗️

This document details the **Hybrid Cloud Architecture** used in SariCoach to deliver a production-grade AI application.

## 1. The "Hybrid" Approach

We split the application into two distinct infrastructure layers:

| Layer | Provider | Spec | Responsibility |
| :--- | :--- | :--- | :--- |
| **Frontend** | **Vercel** | Edge Network | Hosting the React SPA, static assets, and handling SSL termination. |
| **Backend** | **DigitalOcean** | Droplet (8GB RAM) | Hosting the FastAPI Python service, running the AI Agents, and processing DataFrames. |
| **Database** | **Supabase** | Pro Plan | Managed PostgreSQL storage with `pgbouncer` for connection pooling. |

### Architecture Diagram

```mermaid
graph LR
    %% Brand Styling
    classDef user fill:#FCA5A5,stroke:#333,stroke-width:2px;
    classDef vercel fill:#000000,stroke:#fff,stroke-width:2px,color:#fff;
    classDef do fill:#0080FF,stroke:#333,stroke-width:2px,color:#fff;
    classDef db fill:#3ECF8E,stroke:#333,stroke-width:2px,color:#fff;
    classDef ai fill:#8E75B2,stroke:#333,stroke-width:2px,color:#fff;
    classDef connection stroke:#666,stroke-width:2px;

    %% Actors
    User((👤 Store Owner)):::user

    %% Vercel Environment
    subgraph Vercel [⚡ Vercel (Edge Network)]
        direction TB
        Frontend[📱 React / Vite SPA]:::vercel
        Proxy[🛡️ Rewrite Proxy<br/>(vercel.json)]:::vercel
    end

    %% DigitalOcean Environment
    subgraph DigitalOcean [🌊 DigitalOcean Droplet]
        direction TB
        Backend[⚙️ FastAPI Server<br/>(Port 8000)]:::do
        Agent[🤖 Agent Logic<br/>(RAG & Context)]:::do
    end

    %% External Services
    subgraph Services [☁️ Managed Services]
        Supabase[("🗄️ Supabase<br/>(Postgres)")]:::db
        Gemini(("✨ Google Gemini<br/>(1.5 Flash)")):::ai
    end

    %% Flows
    User ==>|HTTPS| Frontend
    Frontend ==>|/api| Proxy
    Proxy -.->|HTTP Tunnel| Backend
    Backend <-->|SQL| Supabase
    Backend --o|Prompt| Agent
    Agent <-->|Inference| Gemini
```

### Why not all Serverless?
AI Agents are stateful and memory-intensive. Loading a retail dataset into Pandas and generating context for an LLM often exceeds the **250MB Memory** and **10s Execution Time** limits of standard Serverless Functions (AWS Lambda / Vercel Functions).

By moving the "Brain" to a dedicated Droplet, we get:
*   **Persistent Memory:** Agents can keep dataframes in RAM.
*   **Long Timeouts:** Complex reasoning chains can take 30s+ without crashing.
*   **Full Control:** We can install system-level dependencies (like `tesseract` or `ffmpeg` in the future).

---

## 2. The Secure Proxy (Networking)

A major challenge in Hybrid apps is **Mixed Content**. The Frontend is HTTPS (Vercel), but the Backend Droplet is often HTTP (unless you manage certs). Browsers block HTTPS -> HTTP requests.

**Solution: Vercel Rewrites**

We use Vercel's edge network as a reverse proxy. The browser talks *only* to Vercel (HTTPS), and Vercel tunnels the request to our Droplet (HTTP) over the backbone network.

**Configuration (`vercel.json`):**

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "http://188.166.237.231:8000/api/:path*"
    }
  ]
}
```

**Flow:**
1.  User requests `https://saricoach.vercel.app/api/coach/ask`
2.  Vercel accepts the request (Secure).
3.  Vercel rewrites it to `http://188.166.237.231:8000/api/coach/ask`.
4.  Droplet processes it and responds.
5.  Vercel relays the response to the user.

---

## 3. Backend Infrastructure (DigitalOcean)

The backend runs on a standard Ubuntu 22.04 Droplet.

*   **IP:** `188.166.237.231`
*   **Process Manager:** `nohup` (Simple background process)
*   **Server:** `uvicorn` (ASGI)

**Deployment Command:**
```bash
nohup uvicorn service.app.main:app --host 0.0.0.0 --port 8000 &
```

This keeps the API alive even after SSH disconnects.

---

## 4. Data Layer (Supabase)

We use **Supabase** as a managed Postgres provider.

*   **Connection Pooling:** Enabled (Port 6543). This is critical because Serverless frontends (or even our multi-worker FastAPI) can open too many direct connections.
*   **Schema:** Defined in `supabase/schema/`.
*   **Seeding:** We use `seed_saricoach_data.py` to generate synthetic retail data (Transactions, Shelf Vision, STT) and push it to the DB.
