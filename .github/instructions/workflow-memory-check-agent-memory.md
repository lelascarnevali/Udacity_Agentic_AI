# Agent Memory Entry

- **Date:** 2026-02-18 (updated 2026-02-25)
- **Topic:** Mandatory memory check before task execution
- **Topics/Tags:** workflow, memory, agent-behavior
- **Source:** User feedback — "Você nunca está avaliando se tem memória para executar tarefa, corrija isso"

## Context

Agent was skipping memory consultation before executing tasks, causing duplicated work and inconsistent outputs. The Step 0 mandatory workflow (read skills catalog + memory index before every task) was created as a direct result of this feedback.

## Decision

The **Step 0 procedure** lives in `AGENTS.md` and in `.github/instructions/workflow-architecture.instructions.md`. This memory file records *why* the rule exists, not the procedure itself.

## Memory-to-Skill Mapping (quick reference)

| Skill | Associated Memory Files |
|:------|:-----------------------|
| `tech-writer` | `study-guide-preference.md` |
| `git-commit` | `terminal-troubleshooting.md` |
| `agent-memory` | `agent-memory-skill-usage-agent-memory.md` |
| Python operations | `virtual-environment-agent-memory.md` |
| GPT / model usage | `gpt5-model-usage-agent-memory.md` |

## References

- Procedure: `AGENTS.md` → Step 0
- Architecture guide: `.github/instructions/workflow-architecture.instructions.md`
- Skills catalog: `.github/skills/README.md`
- Memory index: `.github/agents/memory/README.md`
