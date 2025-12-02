import sqlite3
import json
import os
from typing import List, Dict, Optional, Any

DB_PATH = "orchestrator.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the required schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Core capability definition
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS capabilities (
        id TEXT PRIMARY KEY,
        description TEXT NOT NULL,
        input_schema TEXT NOT NULL,
        runtime_kind TEXT NOT NULL,
        runtime_command TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Provider-specific mapping
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS capability_providers (
        capability_id TEXT NOT NULL,
        provider TEXT NOT NULL,
        name TEXT NOT NULL,
        enabled INTEGER NOT NULL DEFAULT 1,
        extra_config TEXT,
        PRIMARY KEY (capability_id, provider),
        FOREIGN KEY (capability_id) REFERENCES capabilities(id)
    )
    ''')
    
    # External memory / RAG
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS capability_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        capability_id TEXT NOT NULL,
        doc_id TEXT,
        chunk TEXT NOT NULL,
        embedding BLOB,
        metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (capability_id) REFERENCES capabilities(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Orchestrator DB initialized at {DB_PATH}")

def upsert_capability(
    id: str, 
    description: str, 
    input_schema: Dict[str, Any], 
    runtime_kind: str, 
    runtime_command: str = None, 
    tags: List[str] = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO capabilities (id, description, input_schema, runtime_kind, runtime_command, tags, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(id) DO UPDATE SET
        description=excluded.description,
        input_schema=excluded.input_schema,
        runtime_kind=excluded.runtime_kind,
        runtime_command=excluded.runtime_command,
        tags=excluded.tags,
        updated_at=CURRENT_TIMESTAMP
    ''', (
        id, 
        description, 
        json.dumps(input_schema), 
        runtime_kind, 
        runtime_command, 
        json.dumps(tags) if tags else '[]'
    ))
    
    conn.commit()
    conn.close()

def upsert_provider(
    capability_id: str, 
    provider: str, 
    name: str, 
    enabled: bool = True, 
    extra_config: Dict[str, Any] = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO capability_providers (capability_id, provider, name, enabled, extra_config)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(capability_id, provider) DO UPDATE SET
        name=excluded.name,
        enabled=excluded.enabled,
        extra_config=excluded.extra_config
    ''', (
        capability_id, 
        provider, 
        name, 
        1 if enabled else 0, 
        json.dumps(extra_config) if extra_config else '{}'
    ))
    
    conn.commit()
    conn.close()

def get_claude_skills() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT c.id, c.description, c.input_schema, p.name
    FROM capabilities c
    JOIN capability_providers p ON p.capability_id = c.id
    WHERE p.provider = 'claude' AND p.enabled = 1
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return {
        "version": 1,
        "skills": [
            {
                "name": row["name"],
                "description": row["description"],
                "input_schema": json.loads(row["input_schema"])
            }
            for row in rows
        ]
    }

def get_gemini_tools() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT c.id, c.description, c.input_schema, p.name
    FROM capabilities c
    JOIN capability_providers p ON p.capability_id = c.id
    WHERE p.provider = 'gemini' AND p.enabled = 1
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return {
        "tools": [
            {
                "name": row["name"],
                "description": row["description"],
                "input_schema": json.loads(row["input_schema"])
            }
            for row in rows
        ]
    }

def get_codex_ops() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT c.id, c.description, c.input_schema, c.runtime_kind, c.runtime_command, p.name
    FROM capabilities c
    JOIN capability_providers p ON p.capability_id = c.id
    WHERE p.provider = 'codex' AND p.enabled = 1
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return {
        "ops": [
            {
                "id": row["name"],
                "description": row["description"],
                "runtime": row["runtime_kind"],
                "command": row["runtime_command"],
                "input_schema": json.loads(row["input_schema"])
            }
            for row in rows
        ]
    }

if __name__ == "__main__":
    init_db()
