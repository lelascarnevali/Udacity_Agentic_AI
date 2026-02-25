# AI Agent Instructions

This repository hosts Udacity Agentic AI exercises focused on effective prompting for LLM reasoning and planning. Keep guidance minimal, precise, and aligned with the actual workspace.

> **Single source of truth** for all AI assistants (Claude Code, GitHub Copilot, Cursor, etc.).
> Each tool has its own adapter file that maps generic tool references to its native equivalents.

## 1. Repository Context

- Purpose: hands-on notebooks and lightweight utilities for LLM reasoning and planning.
- Stack: macOS + VS Code + Jupyter + Python.

## 2. Repository Structure

```
.
├── .github/                                   # Agent configuration and support assets
│   ├── agents/                                # Custom agents (.agent.md) + memory/
│   │   ├── plan.agent.md                      # "Plan" read-only planning agent
│   │   └── memory/                            # Persistent session learnings
│   ├── instructions/                          # Always-on scoped rules (applyTo glob)
│   │   ├── python-env.instructions.md         # Python/notebook rules
│   │   ├── module-structure.instructions.md   # Exercise/module conventions
│   │   └── workflow-architecture.instructions.md  # Where to put agent workflows
│   ├── prompts/                               # User-invoked slash commands
│   │   ├── documentation_workflow.prompt.md   # /documentation_workflow
│   │   └── commit.prompt.md                   # /commit
│   └── skills/                               # Auto-loaded reusable procedures
│       ├── git-commit/  tech-writer/  agent-memory/
│       ├── prompt-engineering/  skill-creator/  crafting-effective-readmes/
├── .claude/                                   # Claude Code specific agents
│   └── agents/plan.md                         # Plan agent (Claude format)
├── 1_Prompting_for_Effective_LLM_Reasoning_and_Planning/
│   ├── docs/
│   └── exercises/
├── 2_Agentic_Workflows/
│   ├── docs/
│   └── exercises/
├── 3_Building_Agents/
│   ├── docs/
│   └── exercises/
├── 4_Multi-Agent_Systems/
│   ├── docs/
│   └── exercises/
├── scripts/                                   # Reusable Python utilities for notebooks
└── .venv/                                     # Local Python virtual environment (optional)
```

## 3. Operating Workflow (MANDATORY)

> Todas as regras abaixo são obrigatórias em toda tarefa. O Step 0 executa em todo prompt, sem exceção.

### STEP 0: Context and Skill Analysis

Primeiro passo absoluto. Não planeje nem execute nenhuma ação antes de concluí-lo.

1. **ALWAYS Consult Catalogs**: Read `.github/skills/README.md` and `.github/agents/memory/README.md`.
2. **Identify Relevant Knowledge**: Based on the user's request, identify any potentially relevant skills or memories. If any are relevant, you MUST read their `SKILL.md` or memory files.
3. **State Findings**: Your response **MUST** begin with a "Context Analysis" section listing:
   - Skills identified as relevant (e.g., `git-commit`, `tech-writer`).
   - Memories identified as relevant.
   - If none apply, state: "No specific skills or memories were identified as relevant."
   - *Omitting this section is a critical error.*

### STEP 1: ReAct-style Plan & Execute Loop

After completing Step 0:

- Build a plan using your **native task management tool** (see adapter file) that explicitly references rules from loaded skills and memory.
- Execute with a ReAct loop: **Analyze** → **Decide** (skill/memory to apply) → **Act** → **Observe** → **Reflect** and update the task list.
- Before each action, re-evaluate whether an applicable skill or memory should be used.

### Micro-Activities (MANDATORY)

Break work into small, self-contained micro-activities. Each should be a single focused action (e.g., "read file X", "stage files A,B", "apply patch to file Y"). Update the task list after each micro-activity.

### File Editing Rule (MANDATORY)

**NEVER** use terminal commands (`cat`, `echo`, `sed`, `awk`, or similar) to create or edit files. Always use your AI assistant's **native file tools** (see adapter file for mappings).

### Exceptions

Skip the workflow checks only for pure conversational replies that involve no repository or workflow actions, or when explicitly requested by the user.

## 4. Commit Policy (MANDATORY)

1. For every git commit (even small or single-file changes), consult the `git-commit` skill at `.github/skills/git-commit/SKILL.md` and follow its conventional commit message and staging recommendations.
2. When automating commits, prefer `scripts/commit_with_skill.py`. If unavailable, follow the `git-commit` skill manually.
3. Do NOT run destructive git operations (force push, hard reset) without explicit user approval.
4. Only commit when explicitly asked or after user confirmation.

## 5. Language Policy

- `docs/` folders: write in **Portuguese (pt-BR)**.
- Code, variable names, comments: write in **English**.
- Chat responses to the user: reply in **Portuguese (pt-BR)**.

## 6. Workflow Architecture — Where to Put Things

> Full reference: `.github/instructions/workflow-architecture.instructions.md`

Use this table to decide where new agent knowledge belongs:

| Knowledge type | Location | Triggered by |
|---|---|---|
| Always-on project context | `copilot-instructions.md` | Every request |
| Path-scoped coding rules | `instructions/*.instructions.md` | Matching file |
| User-invoked workflow (slash command) | `prompts/*.prompt.md` | `/command` in chat |
| Specialized AI persona | `agents/*.agent.md` | User selects agent |
| Auto-loaded reusable procedure | `skills/<name>/SKILL.md` | AI detects relevance |
| Session learnings / preferences | `agents/memory/*.md` | Agent reads on Step 0 |

**Key rule:** Memory files record *what was learned*, not *what to do*. If a memory file contains a primary procedure, promote it to a Skill or Instruction.

## 8. Skills Catalog

Skills are located in `.github/skills/`. Always consult `.github/skills/README.md` first.

| Skill | When to use |
|---|---|
| `agent-memory` | Recording engineering learnings to `.github/agents/memory/` |
| `crafting-effective-readmes` | Writing or improving README files |
| `git-commit` | Creating conventional commit messages with intelligent staging |
| `prompt-engineering` | Writing/optimizing prompts for agents or LLM interactions |
| `skill-creator` | Creating or updating skills in `.github/skills/` |
| `tech-writer` | Technical writing (study guides, docs) following Strunk & White |

## 9. Agent Memory

Project memory is stored in `.github/agents/memory/`. Always check `.github/agents/memory/README.md` to identify relevant files.

> **Rule:** Memory files record *what was learned*, not *what to do*. Procedures belong in Skills or Instructions.

| Context / Skill | File |
|---|---|
| `tech-writer` skill | `study-guide-preference.md` |
| Python Operations | `virtual-environment-agent-memory.md` |
| Terminal / Git | `terminal-troubleshooting.md` |
| `agent-memory` skill | `agent-memory-skill-usage-agent-memory.md` |
| Workflow Patterns | `workflow-memory-check-agent-memory.md` |
| GPT-5 Models | `gpt5-model-usage-agent-memory.md` |

## 10. Virtual Environment

- Preferred: `.venv/` at workspace root — `python3 -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt`. Deactivate: `deactivate`.
- Details: `.github/instructions/python-env.instructions.md`.

## 11. Code Standards

- **Python**: PEP 8; prefer type hints and concise docstrings; use `black`/`ruff` when applicable.
- **Notebooks**: write formulas in LaTeX within markdown cells.
  - Inline: `$E=mc^2$`
  - Block: `$$\int_a^b f(x)\,dx$$`

## 12. Context Transparency

End every non-trivial response with:

> **Contexto utilizado:** **Skills:** … | **Arquivos:** … | **Memória:** …

List only what was effectively consulted. Omit in purely conversational replies.

---

*See `CLAUDE.md` (Claude Code) or `.github/copilot-instructions.md` (GitHub Copilot) for tool-specific mappings.*
