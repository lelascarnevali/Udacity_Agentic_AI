# Agent Memory Entry

- **Date:** 2026-01-29
- **Topic:** Agent Memory skill usage
- **Topics/Tags:** memory, skill, template
- **Source:** repository skills and documentation workflow

## Context
We introduced the `agent-memory` skill to standardize memory logging. Entries live under `.github/agents/memory` using the `<context>-agent-memory.md` pattern and the memory template.

## Key Insights
- Keep memory entries concise and operational; write for selective loading.
- Use kebab-case context names without dates in filenames; put the date inside the entry.
- Prefer bullets and clear sections for scanability and reuse.

## Decisions / Rules
- Source template from `.github/skills/agent-memory/templates/memory-template.md`.
- Create new entries via `.github/skills/agent-memory/new_memory_entry <context>` or by copying the template manually.
- Do not mirror programming standards or Copilot instructions in memory entries.
- Maintain entries under version control as `.md`; other artifacts remain ignored.

## References
- Skill guide: `.github/skills/agent-memory/SKILL.md`
- Template: `.github/skills/agent-memory/templates/memory-template.md`
- Memory root: `.github/agents/memory`

## Next Actions
- Use this skill to capture learnings from modules 2–4.
- Commit memory entries only on explicit request to avoid noise.
