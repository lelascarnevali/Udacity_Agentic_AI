# GitHub Copilot — Repository Instructions

## Project Summary

`Udacity_Agentic_AI` is a hands-on learning repository for LLM reasoning, planning, and agentic workflows.
**Stack:** macOS · VS Code · Jupyter Notebooks · Python 3 (.venv)

## Repository Layout

```
AGENTS.md                           ← Single source of truth for all AI agents
CLAUDE.md                           ← Claude Code tool adapter
.github/
  copilot-instructions.md           ← This file (Copilot instructions + tool adapter)
  agents/plan.agent.md              ← Custom "Plan" agent
  instructions/python-env.instructions.md  ← Python-specific rules (auto-applied)
  prompts/documentation_workflow.prompt.md ← /documentation_workflow slash command
  skills/                           ← Agent skills (agent-memory, git-commit, tech-writer, …)
  agents/memory/                    ← Persistent memory files
1_Prompting_for_Effective_LLM_Reasoning_and_Planning/
2_Agentic_Workflows/
3_Building_Agents/
4_Multi-Agent_Systems/
```

## Critical Rules (from AGENTS.md)

1. **Always start every task** with Step 0: read `.github/skills/README.md` and `.github/agents/memory/README.md`.
2. **Never use terminal commands** to create or edit files — use native file tools only.
3. **Language policy:** docs/ → Portuguese (pt-BR) | code/comments → English | chat → Portuguese (pt-BR).
4. **Commits** → always follow `.github/skills/git-commit/SKILL.md` or use `/commit` slash command.
5. **Python env** → `.venv/` at workspace root (`source .venv/bin/activate`).

## Workflow Architecture (quick reference)

| Want to… | Use |
|---|---|
| Apply rules to all requests | `copilot-instructions.md` |
| Apply rules to specific files | `instructions/*.instructions.md` |
| Create a `/slash-command` | `prompts/*.prompt.md` |
| Create a specialized AI persona | `agents/*.agent.md` |
| Auto-load a reusable procedure | `skills/<name>/SKILL.md` |
| Record a session learning | `agents/memory/*.md` |

> Full reference: `.github/instructions/workflow-architecture.instructions.md`

## VS Code Tool Mapping

> Full instructions are in [`AGENTS.md`](../AGENTS.md). Use the mappings below for VS Code / Copilot equivalents.

| Generic reference in AGENTS.md | VS Code / Copilot tool |
|---|---|
| Native task management tool | `manage_todo_list` |
| Native file creation tool | `create_file` |
| Native file editing tool | `replace_string_in_file` |
| Native file reading tool | `read_file` |
| Native notebook editing tool | `edit_notebook_file` |
| Native file search tool | `list_dir` / `file_search` |
| Native content search tool | `grep_search` |
| Shell / terminal commands | `run_in_terminal` |

## Skills Integration

Skills are in `.github/skills/`. See `.github/skills/README.md` for the full catalog.
