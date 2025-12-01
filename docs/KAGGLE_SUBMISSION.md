# SariCoach: Pocket Enterprise Intelligence for Sari-Sari Stores

### 🔹 One-sentence subtitle
An AI retail coach that turns live Supabase transaction data into plain-language guidance for neighborhood sari-sari stores.

### 🔹 Suggested Track
**Agents for Good**

---

### 🔹 Project Description

#### Problem Statement — what problem are we solving, and why it matters
In the Philippines, neighborhood “sari-sari” stores are everywhere, but they run on **gut feel**, not data.

Owners juggle supplier credit, expiring stock, and daily cash flow with:
* No BI tools or data team
* Paper notebooks or basic POS apps
* Zero visibility into *which* products drive profit, *when* demand peaks, or *where* they’re about to stock out

Enterprise ERPs and dashboards (Odoo, SAP, Power BI) exist, but they’re too complex and expensive for a small store with one phone and spotty internet.

**SariCoach** tries to close that gap: give a sari-sari owner the feeling of having a personal analyst and consultant **in their phone**, using the same kind of metrics a big chain would use.

#### Why agents? — why an agent is the right solution
A static dashboard can show charts, but sari-sari owners don’t have time to interpret them. They need **“what should I do?”**, not “here’s a graph.”

Agents are the right fit because they can:
1. **Pull context from live data**
   Before answering, the agent queries Supabase for revenue, volume, top items, low-stock SKUs, and hourly patterns.
2. **Reason over multiple signals**
   The agent combines transactions with synthetic “future” signals like shelf-vision events and STT demand flags (designed into the schema), so the system can later be extended to vision/audio without changing the contract.
3. **Speak in plain language**
   The CoachAgent turns SQL metrics into short, Tagalog-friendly coaching like:
   *“Bebidas traffic peaks 6–8 PM. You’re often low on Coke 1.5L by 7 PM; add 1 extra crate in the next order.”*
4. **Support different roles**
   The same agent stack can serve a store owner, a distributor, or a brand manager just by changing the prompt and filters, without rebuilding the UI.

So instead of “a React chart app,” SariCoach is a **Gemini-powered agent** that happens to have a mobile-first UI.

#### What you created — architecture & flow
The project is fully implemented as a **Supabase + FastAPI + Vercel** stack. No fake APIs; everything in the app talks to a real backend.

**1. Data Layer – Supabase (PostgreSQL)**
Canonical schema (`kaggle.*` / `public.*`) includes:
* `brands`, `products`, `stores`
* `transactions`, `transaction_lines`
* `foot_traffic_daily`, `weather_daily`
* `shelf_vision_events`, `stt_events`

Supabase hosts the production database. A `seed_saricoach_data.py` script can:
* Generate a multimodal retail dataset from Kaggle-style CSVs **or**
* Emit `seed_saricoach.sql` for seeding Supabase directly

For Kaggle judges, the same schema can be replayed as CSVs in a notebook, but the primary runtime is live Supabase.

**2. Backend – FastAPI on DigitalOcean**
Directory: `service/`
* **API Layer**
  * `GET /api/store/{id}/summary`: Aggregates today’s revenue, transactions, avg basket, top item, and hourly traffic from Supabase.
  * `GET /api/store/{id}/weekly-insights`: Weekly revenue trend, top movers, category mix.
  * `POST /api/coach/recommendations`: Accepts `store_id` + optional focus (`brand_id`, `category`) and returns structured recommendations.

* **Agent Layer (inside the service)**
  * `PlannerAgent`: Maps UI intents (“Daily view”, “Weekly insights”, “Ask Coach”) to data queries + coach calls.
  * `DataAnalystAgent`: Builds a feature frame from Supabase data: store × day × brand with sales, facings, OOS flags, STT mentions, weather, and traffic indices.
  * `CoachAgent` (Gemini 1.5 Flash via Google AI SDK): Takes the feature frame + natural-language question and returns insights, actions, and risks.

If `SARICOACH_GOOGLE_API_KEY` is missing, the service falls back to a **deterministic stub** so the API stays runnable for reviewers and CI.

**3. Frontend – React + Vite + Tailwind on Vercel**
Directory: `dashboard/`
The UI is designed as a **mobile-first, bottom-tab app** that mirrors iOS design patterns:
* **Home**: Today’s KPIs (Revenue, Transactions, Avg Basket, Top Item), Hourly traffic chart, “Ask Coach” button.
* **Insights**: Weekly revenue trend line, Top movers list, Sales by category bars.
* **History**: Timeline of daily batch totals, walk-in sales, and supplier payments.
* **Settings**: Store profile, Data source toggle, Future flags.

The dashboard reads `VITE_API_URL` from environment variables (Vercel + local `.env`) and talks only to the FastAPI service. All screens you see in the screenshots are **wired to real endpoints**.

#### Demo — how SariCoach behaves
A typical flow:
1. Owner opens **Home** → the app calls `/api/store/1/summary`. Shows today’s KPIs and an empty traffic chart if there’s no data yet.
2. After seeding Supabase, **Insights** shows a full weekly curve, top movers, and category bars from live data.
3. Tapping **Ask Coach** sends `store_id`, last 7 days of KPIs, and any filters to the backend, which in turn calls Gemini through the `CoachAgent`.
4. The user receives a compact briefing such as: *“Revenue up 12.5% vs last week driven by beverages; cigarettes down 5%. Expect rain later today — increase facings for hot drinks and keep backup stock for instant noodles.”*

Everything is grounded in real rows in Supabase.

#### The Build — tools & concepts from the course
From the Agents Intensive, SariCoach directly applies at least **three key concepts**:
1. **Context Engineering**: Before each agent call, the backend constructs a structured context: JSON snippets of KPIs, trends, and feature rows. The system prompt instructs Gemini to reason only over this injected data.
2. **Tool-using Agents**: The agent stack treats Supabase queries as tools. Planner → calls DataAnalyst tools → passes summarized frames to CoachAgent.
3. **Prototype → Production Deployment**: Instead of remaining in a notebook, SariCoach is deployed as React/Vercel frontend, FastAPI on DigitalOcean, and Supabase as managed Postgres backend. Environment variables are configured on Vercel and the Droplet; **no secrets are committed to Git**.

We also added basic testing:
* `verify_brain.py` sanity-checks schema and seed data.
* Manual E2E tests validate that each page renders and that API error states surface cleanly.

#### If I had more time…
If I continue this project, I would:
* Plug in **real vision and STT streams** (e.g., on-device snapshots and phone call transcripts) into the existing `shelf_vision_events` and `stt_events` tables.
* Add a **lightweight offline-first mode** so the app can cache the last 7 days even with unreliable connectivity.
* Build a **scheduled “Daily Coach Briefing”** that sends a morning SMS or WhatsApp summary generated by the agent.
* Extend agents to serve **distributors and brand managers**, not just store owners, using the same Supabase data model but different prompts and filters.

---

### 🔹 Project Links
* **GitHub (code + docs):** `https://github.com/jgtolentino/saricoach-retail-insights`
* **Live App (Vercel):** `https://agents-intensive-saricoach.vercel.app`
