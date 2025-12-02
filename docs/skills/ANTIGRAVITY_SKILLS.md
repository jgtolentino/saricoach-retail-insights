# Antigravity Productivity Stack & Skills 🚀

This document defines the "Knowledge Base" and "Skills Binding" for the SariCoach project, enabling 10x productivity via the Antigravity agent workflow.

## 1. 🧠 Gemini 3 & Prompting Strategies
*Reference: [Gemini API Docs](https://ai.google.dev/gemini-api/docs/gemini-3)*

To maximize agent performance, we utilize **Gemini 3** capabilities:
*   **Long Context:** We can ingest entire documentation sets (Supabase docs, n8n schemas) into the context window.
*   **Reasoning:** Use "Chain of Thought" prompting for complex architectural decisions (e.g., "Should this logic live in a Postgres Trigger or an Edge Function?").
*   **Multimodality:** We can process screenshots of dashboards or diagrams to generate corresponding code.

## 2. ⚡ Supabase & Edge Architecture

### Database (PostgreSQL)
*   **Schema Management:** All schema changes must be versioned in `supabase/migrations`.
*   **Type Safety:** Use `supabase gen types` to keep TypeScript interfaces in sync with the DB.

### Edge Functions
*   **Location:** `supabase/functions/`
*   **Runtime:** Deno (standard for Supabase Edge).
*   **Use Cases:**
    *   Webhooks (e.g., Stripe, n8n triggers).
    *   AI inference (calling Gemini API securely).
    *   Latency-sensitive logic (closer to user).

### Cron Jobs
*   **Implementation:** Use `pg_cron` extensions within the database for scheduled tasks (e.g., daily aggregations).
*   **Management:** Define cron schedules in SQL migrations:
    ```sql
    select cron.schedule('daily-summary', '0 0 * * *', 'select generate_daily_summary()');
    ```

## 3. 🤖 Automation & Orchestration (n8n)

*   **Role:** n8n handles complex, multi-step workflows that don't require sub-millisecond latency (e.g., email sequences, cross-platform syncing).
*   **Integration:**
    *   **Trigger:** Webhook from Supabase Database Webhooks or Edge Functions.
    *   **Action:** Update Supabase records or call external APIs.

## 4. 🛠️ Makefile Automation

We use a `Makefile` at the root to standardize common developer tasks ("Skills Binding").

**Standard Commands:**
*   `make setup`: Install dependencies (Python, Node, Supabase CLI).
*   `make dev`: Start local development stack (Frontend + Backend + Supabase).
*   `make db-reset`: Reset local database and apply seeds.
*   `make deploy`: Deploy to production (Vercel + Supabase).
*   `make test`: Run full test suite.

## 5. 📂 Project Structure Binding

*   `/supabase`: Database & Edge Functions.
*   `/dashboard`: Frontend (React/Vite).
*   `/service`: Python Backend (FastAPI/Agent).
*   `/workflows`: n8n workflow JSON exports.

---
*This file serves as the "System Context" for Antigravity operations in this workspace.*
