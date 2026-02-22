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

**YOU MUST follow these steps in order for EVERY task. No exceptions.**

**STEP 0: CONTEXT AND SKILL ANALYSIS (NON-NEGOTIABLE)**
This is the absolute first step. Do not plan or execute any other action until this is complete.
1.  **Consult Catalogs**: Read `.github/skills/README.md` and `.github/agents/memory/README.md`.
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

This policy enforces always checking skills and memory, applying ReAct reasoning, and using micro-activities so automated agents behave consistently and safely.

### Execution Best Practices
- **Workflow:** Read Indices (`README.md`s) → Read Specific Files → Plan (`manage_todo_list`) → Execute.
- **File Editing Rule (MANDATORY):** NEVER use terminal commands (like `cat`, `echo`, `sed`) to create or edit files. ALWAYS use VS Code tools (`create_file`, `replace_string_in_file`, `edit_notebook_file`).
- Be specific with meaningful names (functions, variables, commit messages)
- Provide top-level context comments for complex implementations
- Use precise, domain-specific terms likely to appear in the codebase
- Execute changes minimally; bundle commits logically
- Only commit when explicitly asked or after confirmation

## 3.2 Language Policy
- Documentation, code comments, and prompt design: write in English.
- Chat responses to the user: reply in Portuguese (pt-BR).
- Keep examples consistent: internal artifacts in English; communication in Portuguese.


## 4. Virtual Environment
- Preferred: local virtualenv at `.venv/`.
- Setup on macOS:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python --version
pip --version
```

- Deactivate:

```sh
deactivate
```

## 5. Standards
- Python: follow PEP 8; prefer type hints and concise docstrings; use `black`/`ruff` when applicable.
- Notebooks: write formulas in LaTeX within markdown cells.
  - Inline: `$E=mc^2$`
  - Block: `$$\int_a^b f(x)\,dx$$`

## 6. Context Transparency
At the end of each response, always include a section showing which resources were used:

```markdown
---
**Contexto utilizado:**
- **Skills:** [list of skills from .github/skills/ that were referenced.]
- **Arquivos:** [list of files that were read or modified]
- **Memória:** [agent memory files from .github/agents/memory/ if consulted]
```

Guidelines:
- Only list skills if explicitly consulted from `.github/skills/`
- List all files read with `read_file` or modified with editing tools
- Include memory files only if actually accessed
- Omit the section entirely for simple conversational responses that don't use external resources
- Keep the format concise and scannable

— End of instructions —
