---
name: agent-memory-bmad
description: BMAD-style agent memory logging for engineering learnings using Markdown entries.
---

# Agent Memory (BMAD)

This skill standardizes how to capture persistent agent learnings using the BMAD method.

## When to Use
- After completing a task, design decision, or investigation with lessons worth retaining
- When you need reproducible, loadable notes for agents across sessions
- To keep README focused on setup/usage while memory lives separately

## Location & Naming
- Memory root: `.github/agents/memory/`
- Filename pattern: `<context>-agent-memory.md` (kebab-case; no spaces)
- Date: include inside the entry body, not in the filename

## Template
Start from the BMAD template:
- Path: `.github/skills/agent-memory-bmad/templates/bmad-template.md`
- Copy to `.github/agents/memory/<context>-agent-memory.md`

## Structure (BMAD-aligned)
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
cp .github/skills/agent-memory-bmad/templates/bmad-template.md \
   .github/agents/memory/${ctx}-agent-memory.md
# Edit the new file and commit
code .github/agents/memory/${ctx}-agent-memory.md
```

## Conventions
- Keep entries concise, factual, and operational; prefer bullets
- Reference exact files/paths; avoid code dumps
- Do not duplicate programming standards or Copilot instructions here
- `.github/agents/memory/.gitignore` tracks only `.md` and `.gitkeep`

## References
- BMAD Method: https://docs.bmad-method.org/
- BMAD (LLM-optimized): https://docs.bmad-method.org/llms-full.txt
- Agent Memory & Sidecar: https://deepwiki.com/bmad-code-org/BMAD-METHOD/7.4-agent-memory-and-sidecar-system
