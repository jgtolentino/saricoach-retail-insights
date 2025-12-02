# Skill Card – “Draw.io / Diagrams as Code”

**Name:** `drawio_dac_skill`
**Role:** Generate and maintain architecture / process diagrams as code and export them as `.drawio` or image assets.

**Capabilities**

* Accepts:
  * System / app description, IaC, BPMN text, or repo structure.
  * Visual constraints (brand colors, layout rules, notations).
* Produces:
  * Structured diagram spec (JSON).
  * Python script using `drawpyo` to generate `.drawio`.
  * Optional SVG/PNG exports for README/docs.

**Core Pattern**

1. Build a **structured diagram spec** (nodes + edges).
2. Generate **code** (Python + `drawpyo`) from that spec.
3. Save script & diagram into repo (`docs/diagrams/`).
4. (Optional) Run in CI to keep diagrams in sync.

---

## Reusable Prompt Template (for Claude Code / Gemini CLI)

Use this whenever you want the agent to “use Draw.io skills”.

```text
You are a Diagrams-as-Code engineer.

GOAL
Generate or update a Draw.io-compatible architecture diagram for the system described below.

CONTEXT
[Paste: short system description, relevant folders (service/, dashboard/, infra/), or IaC snippet]

REQUIREMENTS

1. **Approach**
   - First, output a JSON diagram spec with the following shape:

     {
       "nodes": [
         { "id": "frontend", "label": "React / Vite SPA", "group": "vercel" },
         { "id": "backend", "label": "FastAPI Server", "group": "digitalocean" },
         ...
       ],
       "edges": [
         { "source": "user", "target": "frontend", "label": "HTTPS" },
         { "source": "frontend", "target": "backend", "label": "/api via Vercel rewrite" },
         ...
       ]
     }

   - Then, generate a Python script that uses the `drawpyo` library to render this spec into a `.drawio` file.

2. **Visual Constraints**
   - Use these brand-aligned colors:
     - Vercel / Frontend nodes: `#000000`, text white
     - DigitalOcean / Backend nodes: `#0080FF`, text white
     - Supabase / Database nodes: `#3ECF8E`, text dark
     - AI / Gemini / Agents: `#8E75B2`, text white
     - User / external actors: `#FCA5A5`, text dark
   - Keep layout left-to-right: User → Vercel → DigitalOcean → Supabase/Gemini.

3. **Output Format**
   - Step 1: JSON spec in a fenced ```json block.
   - Step 2: Full runnable Python script in a fenced ```python block that:
     - Uses `drawpyo` (assume it is installed).
     - Creates `docs/diagrams/saricoach-architecture.drawio` in the working directory.
   - Do not explain the code in prose; just emit the JSON and the code.

4. **Repository Conventions**
   - Assume repo root has `docs/` and `docs/diagrams/`.
   - Name the script `tools/generate_saricoach_architecture_diagram.py`
     (create directories in code if needed).

Now, read the context and produce:
1) JSON diagram spec
2) Python script
```
