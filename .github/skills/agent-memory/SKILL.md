---
name: agent-memory
description: Agent memory logging for engineering learnings using Markdown entries.
---

# Agent Memory

This skill standardizes how to capture persistent agent learnings using a concise, consistent memory format.

## When to Use
- After completing a task, design decision, or investigation with lessons worth retaining
- When you need reproducible, loadable notes for agents across sessions
- To keep README focused on setup/usage while memory lives separately

## Location & Naming
- Memory root: `.github/agents/memory/`
- Filename pattern: `<context>-agent-memory.md` (kebab-case; no spaces)
- Date: include inside the entry body, not in the filename

## Template
Start from the memory template:
- Path: `.github/skills/agent-memory/assets/templates/memory-template.md`
- Copy to `.github/agents/memory/<context>-agent-memory.md`

## Structure
- Metadata (top): Date, Topic, Topics/Tags, Source
- Context: what changed and why it matters
- Key Insights: distilled lessons/findings
- Decisions/Rules: standards and trade-offs
- References: internal paths and external links
- Next Actions: follow-ups to validate or extend
- Optional: Learned Patterns, Tags

## Quick Create (macOS/Linux)
```bash
# From repo root
ctx="role-based-prompting"
.github/skills/agent-memory/scripts/new_memory_entry "${ctx}"
```

## Conventions
- Keep entries concise, factual, and operational; prefer bullets
- Reference exact files/paths; avoid code dumps
- Do not duplicate programming standards or Copilot instructions here
- `.github/agents/memory/.gitignore` tracks only `.md` and `.gitkeep`

## References
- Memory conventions: `.github/agents/memory/README.md`
- Template: `.github/skills/agent-memory/templates/memory-template.md`
