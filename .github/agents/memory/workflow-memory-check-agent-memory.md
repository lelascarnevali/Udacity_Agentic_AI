Date: 2026-03-23
Topic: workflow memory check
Tags: workflow, memory, documentation, repository-integrity
Source: Repository documentation workflow and memory index maintenance

## Context

The memory index referenced `workflow-memory-check-agent-memory.md`, but the file was missing from `.github/agents/memory/`.
This created a mismatch between the documented workflow and the actual repository state.

## Key Insights

- Step 0 depends on both the skills catalog and the memory index being internally consistent.
- Broken references inside `.github/agents/memory/README.md` degrade the reliability of the mandatory context-loading workflow.
- Memory files should capture why a workflow rule exists, while procedures remain in `AGENTS.md`, skills, or instructions.

## Skill-to-Memory Quick Reference

| Context / Skill | Memory File | Purpose |
| --- | --- | --- |
| `tech-writer` | `study-guide-preference.md` | Documentation structure, formatting, and navigation conventions. |
| Python / Jupyter | `virtual-environment-agent-memory.md` | Environment and kernel alignment notes. |
| Terminal / Git | `terminal-troubleshooting.md` | Recurrent shell and command execution pitfalls. |
| `agent-memory` | `agent-memory-skill-usage-agent-memory.md` | Naming, template, and index maintenance rules for memory entries. |
| Workflow patterns | `workflow-memory-check-agent-memory.md` | Why Step 0 exists and how to validate memory integrity before work. |
| GPT-5 / Models | `gpt5-model-usage-agent-memory.md` | Model usage differences and fallback guidance. |

## Decisions/Rules

- Keep `.github/agents/memory/README.md` aligned with the files that actually exist in the directory.
- Use this memory entry as the reference for why Step 0 includes a memory check before non-trivial work.
- Treat missing memory files referenced by the index as repository maintenance issues that should be corrected immediately.

## References

- `.github/agents/memory/README.md`
- `AGENTS.md`
- `.github/prompts/documentation_workflow.prompt.md`

## Next Actions

- Periodically verify that every entry in the memory index resolves to a real file.
- When creating new memory entries, update the index in the same change set.
