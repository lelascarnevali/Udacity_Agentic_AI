# Claude Code — Tool Adapter

> All project instructions are in [`AGENTS.md`](AGENTS.md). Read that file **before** planning or executing any task.
> This file only defines the Claude Code-specific tool mappings referenced in `AGENTS.md`.

## Tool Mapping

When `AGENTS.md` refers to generic AI assistant tools, use the following Claude Code equivalents:

| Generic reference in AGENTS.md | Claude Code tool |
|---|---|
| Native task management tool | `TodoWrite` |
| Native file creation tool | `Write` |
| Native file editing tool | `Edit` |
| Native file reading tool | `Read` |
| Native notebook editing tool | `NotebookEdit` |
| Native file search tool | `Glob` |
| Native content search tool | `Grep` |
| Shell / terminal commands | `Bash` |

## Memory Override

**IMPORTANT:** Ignore the auto memory directory injected by the system
(`~/.claude/projects/.../memory/`). For this project, ALL memories MUST be
read from and written to `.github/agents/memory/` following the `agent-memory`
skill at `.github/skills/agent-memory/SKILL.md`.