# Agent Memory Index

This directory stores **persistent learnings, preferences, and troubleshooting notes** captured across sessions.

> **Rule:** Memory files record *what was learned*, not *what to do*.
> Procedures belong in `.github/skills/` (auto-loaded) or `.github/instructions/` (always-on rules).

When performing tasks, check this index to identify relevant memory files based on context or skill.

| Context / Skill | Memory File | What it contains |
| :--- | :--- | :--- |
| `tech-writer` skill | [`study-guide-preference.md`](study-guide-preference.md) | User style preferences: emojis, LaTeX, tables, code-first structure |
| Python / Jupyter | [`virtual-environment-agent-memory.md`](virtual-environment-agent-memory.md) | venv setup quirks, uv usage, kernel matching |
| Terminal / Git | [`terminal-troubleshooting.md`](terminal-troubleshooting.md) | Heredoc trap, known terminal errors and fixes |
| `agent-memory` skill | [`agent-memory-skill-usage-agent-memory.md`](agent-memory-skill-usage-agent-memory.md) | Naming conventions, template path, commit policy for memory files |
| Workflow patterns | [`workflow-memory-check-agent-memory.md`](workflow-memory-check-agent-memory.md) | *Why* Step 0 was created + skill-to-memory quick-reference table |
| GPT-5 / Models | [`gpt5-model-usage-agent-memory.md`](gpt5-model-usage-agent-memory.md) | API differences (Responses vs Chat Completions), reasoning params, fallback strategy |

## Where procedures live (not here)

| Procedure | Location |
|---|---|
| Step 0 mandatory workflow | `AGENTS.md` → Section 3 |
| Where to put agent knowledge | `.github/instructions/workflow-architecture.instructions.md` |
| How to write memory entries | `.github/skills/agent-memory/SKILL.md` |
| How to commit | `.github/skills/git-commit/SKILL.md` |
