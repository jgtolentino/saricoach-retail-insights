import json
import yaml
import os
from capabilities_db import get_claude_skills, get_gemini_tools, get_codex_ops

SKILLS_DIR = "skills"

def gen_capabilities():
    print("🔄 Generating Capabilities Views...")
    
    # 1. Claude Skills (YAML)
    claude_data = get_claude_skills()
    with open(os.path.join(SKILLS_DIR, "claude.skills.yaml"), "w") as f:
        yaml.dump(claude_data, f, sort_keys=False)
    print(f"✅ Generated {SKILLS_DIR}/claude.skills.yaml")
    
    # 2. Gemini Tools (JSON)
    gemini_data = get_gemini_tools()
    with open(os.path.join(SKILLS_DIR, "gemini.tools.json"), "w") as f:
        json.dump(gemini_data, f, indent=2)
    print(f"✅ Generated {SKILLS_DIR}/gemini.tools.json")
    
    # 3. Codex Ops (YAML)
    codex_data = get_codex_ops()
    with open(os.path.join(SKILLS_DIR, "codex.ops.yaml"), "w") as f:
        yaml.dump(codex_data, f, sort_keys=False)
    print(f"✅ Generated {SKILLS_DIR}/codex.ops.yaml")

if __name__ == "__main__":
    gen_capabilities()
