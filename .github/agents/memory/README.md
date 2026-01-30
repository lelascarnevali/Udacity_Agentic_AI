# Agent Memory

Persistent learnings for agents live here as Markdown files.

## Conventions
- **Scope:** Record engineering learnings, decisions, and context; avoid code dumps.
- **Format:** Use `templates/learning-template.md`.
- **Naming:** `<context>-agent-memory.md` (e.g., `readme-agent-memory.md`, `workflow-routing-agent-memory.md`).
- **Date:** Include the date inside the entry body, not in the filename.
- **Privacy:** Version only `.md` entries; other artifacts are ignored by `.gitignore`.
- **Decoupling:** Do not mirror programming standards or Copilot instructions here.

## Suggested Workflow
1. Generate a new entry via the helper script (recommended):
	- `python scripts/new_memory_entry.py --context "<context>" --topic "<topic>" --tags tag1 tag2 --source "<source>" --agent github-copilot --yaml`
	- This creates `<context>-agent-memory.md` using the BMAD template and optional YAML frontmatter.
2. Alternatively, copy the template to a context-based filename and fill sections manually:
	- Use `templates/bmad-template.md` and replace placeholders.
3. Commit with `docs(agents): add memory entry`.
