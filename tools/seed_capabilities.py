from capabilities_db import init_db, upsert_capability, upsert_provider

def seed_data():
    print("🌱 Seeding Capabilities Registry...")
    init_db()
    
    # 1. knowledge.refresh
    upsert_capability(
        id="knowledge.refresh",
        description="Refresh knowledge base from docs and push embeddings to Supabase.",
        input_schema={
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "enum": ["docs", "erd", "tickets", "mixed"]
                }
            },
            "required": ["source"]
        },
        runtime_kind="make",
        runtime_command="make n8n-trigger-knowledge-refresh",
        tags=["knowledge", "rag", "cron"]
    )
    
    upsert_provider("knowledge.refresh", "claude", "knowledge.refresh")
    upsert_provider("knowledge.refresh", "gemini", "knowledge_refresh")
    upsert_provider("knowledge.refresh", "codex", "knowledge.refresh")
    
    # 2. supabase.migrate
    upsert_capability(
        id="supabase.migrate",
        description="Apply Supabase migrations (db push) for this project.",
        input_schema={
            "type": "object",
            "properties": {
                "dryRun": {
                    "type": "boolean",
                    "default": False
                }
            }
        },
        runtime_kind="make",
        runtime_command="make supabase-db-migrate",
        tags=["supabase", "db", "migration"]
    )
    
    upsert_provider("supabase.migrate", "claude", "supabase.migrate")
    upsert_provider("supabase.migrate", "gemini", "supabase_migrate")
    upsert_provider("supabase.migrate", "codex", "supabase.migrate")
    
    print("✅ Capabilities seeded.")

if __name__ == "__main__":
    seed_data()
