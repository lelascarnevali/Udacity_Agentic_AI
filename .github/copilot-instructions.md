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

### Skill-First with Memory Context (MANDATORY)
**BEFORE creating a plan or executing ANY task (including tasks that appear trivial):**

1. **Consult Knowledge Indices (always)**:
   - **Skills Catalog**: Read `.github/skills/README.md` to identify available capabilities.
   - **Memory Index**: Read `.github/agents/memory/README.md` to identify relevant past learnings or preferences.

2. **Activate Specific Knowledge (when present)**:
   - Read the specific skill files that look relevant (e.g., `.github/skills/*/SKILL.md`).
   - Read the specific memory files that look relevant (e.g., `.github/agents/memory/*-memory.md`).

3. **ReAct-style Plan & Execute Loop**:
   - Build a plan using `manage_todo_list` that explicitly references rules or steps from any loaded skills and memory.
   - Use a ReAct loop for execution: **Analyze** the task and repo state → **Decide** which skill/memory (if any) to apply and which micro-action to take → **Act** (use tools) → **Observe** results → **Reflect** and update plan.
   - Before each action, re-evaluate whether an applicable skill or memory should be used.

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
