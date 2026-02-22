# GitHub Copilot Instructions

This repository hosts Udacity Agentic AI exercises focused on effective prompting for LLM reasoning and planning. Keep guidance minimal, precise, and aligned with the actual workspace.

## 1. Repository Context
- Purpose: hands-on notebooks and lightweight utilities for LLM reasoning and planning.
- Stack: macOS + VS Code + Jupyter + Python.

## 2. Repository Structure
```
.
├── .github/                                   # Copilot configuration and support assets
│   └── skills/                                # Copilot "skills" docs and helper scripts
├── 1_Prompting_for_Effective_LLM_Reasoning_and_Planning/ # Module 1: Prompting foundations
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 2_Agentic_Workflows/                       # Module 2: Designing agentic workflows
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 3_Building_Agents/                         # Module 3: Implementing agents
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 4_Multi-Agent_Systems/                     # Module 4: Multi-agent systems
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── scripts/                                   # Reusable Python utilities for notebooks
└── .venv/                                     # Local Python virtual environment (optional)
```

## 3. Skills (skill.sh)
- integrate Copilot "skills" via a shell script.
- Skills location: `.github/skills/`.

## 3.1 Operating Workflow

### Core Workflow (MANDATORY)

> Todas as regras abaixo são obrigatórias em toda tarefa. Step 0 executa em todo prompt, sem exceção.

**STEP 0: CONTEXT AND SKILL ANALYSIS**
Primeiro passo absoluto. Não planeje nem execute nenhuma ação antes de concluí-lo.
1.  **ALWAYS Consult Catalogs**: Read `.github/skills/README.md` and `.github/agents/memory/README.md`.
2.  **Identify Relevant Knowledge**: Based on the user's request, identify any potentially relevant skills or memories. If any are relevant, you MUST read their `SKILL.md` or memory files.
3.  **State Findings in Your Plan**: Your execution plan **MUST** begin with a "Context Analysis" section that lists:
    *   The skills you identified as relevant (e.g., `git-commit`, `tech-writer`).
    *   The memories you identified as relevant.
    *   If no specific skills/memories seem relevant, you must state: "No specific skills or memories were identified as relevant."
    *   *Failure to include this section in your plan is a critical error.*

**STEP 1: ReAct-style Plan & Execute Loop**:
   - After completing Step 0, build a plan using `manage_todo_list` that explicitly references rules or steps from any loaded skills and memory.
   - Use a ReAct loop for execution: **Analyze** the task and repo state → **Decide** which skill/memory (if any) to apply and which micro-action to take → **Act** (use tools) → **Observe** results → **Reflect** and update plan.
   - Before each action, re-evaluate whether an applicable skill or memory should be used.

**COMMIT POLICY (REPOSITORY):**
1. For every git commit made by this agent (even for small or single-file changes), the agent MUST use the `git-commit` skill from `.github/skills/git-commit/SKILL.md` to generate the commit message and follow its staging recommendations.
2. When automating commits, prefer using the repository helper script `scripts/commit_with_skill.py` which implements the `git-commit` heuristics. If the script is not available, the agent must still consult the `git-commit` skill and follow its workflow manually.
3. Do NOT run destructive git operations (force push, hard reset) without explicit user approval.

4. **Micro-Activities (MANDATORY)**:
   - Break work into small, self-contained micro-activities to avoid exceeding the LLM context window. Each micro-activity should be a single focused action (e.g., "read file X", "generate diff summary", "stage files A,B", "apply patch to file Y").
   - After completing each micro-activity, record progress in `manage_todo_list` and re-check skills/memories for newly relevant guidance.

5. **Exceptions**:
   - Only skip the above checks for pure conversational replies that do not involve repository or workflow actions and when explicitly requested by the user.

### Execution Best Practices
- **Workflow:** Read Indices (`README.md`s) → Read Specific Files → Plan (`manage_todo_list`) → Execute.
- **File Editing Rule (MANDATORY):** NEVER use terminal commands (like `cat`, `echo`, `sed`) to create or edit files. ALWAYS use VS Code tools (`create_file`, `replace_string_in_file`, `edit_notebook_file`).
- Be specific with meaningful names (functions, variables, commit messages)
- Provide top-level context comments for complex implementations
- Use precise, domain-specific terms likely to appear in the codebase
- Execute changes minimally; bundle commits logically
- Only commit when explicitly asked or after confirmation

## 3.2 Language Policy
- `docs/` folders: write in Portuguese (pt-BR).
- Code, variable names, comments: write in English.
- Chat responses to the user: reply in Portuguese (pt-BR).


## 4. Virtual Environment
- Preferred: local virtualenv at `.venv/` — `python3 -m venv .venv && source .venv/bin/activate`.
- Install deps: `pip install -r requirements.txt`. Deactivate with `deactivate`.
- Details: see `.github/instructions/python-env.instructions.md`.

## 5. Standards
- Python: follow PEP 8; prefer type hints and concise docstrings; use `black`/`ruff` when applicable.
- Notebooks: write formulas in LaTeX within markdown cells.
  - Inline: `$E=mc^2$`
  - Block: `$$\int_a^b f(x)\,dx$$`

## 6. Context Transparency
End every non-trivial response with:

> **Contexto utilizado:** **Skills:** … | **Arquivos:** … | **Memória:** …

Liste apenas o que foi efetivamente consultado. Omita em respostas puramente conversacionais.

— End of instructions —
