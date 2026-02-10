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

### Skill-First Approach
**MANDATORY**: Before executing ANY task, check for relevant skills:
1. **Always read `.github/skills/README.md` first** - comprehensive catalog of all available skills
2. Search for relevant skill using catalog categories or semantic search
3. When a skill exists, **follow its documented workflow** - do NOT use direct terminal commands
4. Skills are authoritative - they contain validated, tested procedures

### Context Gathering
- Check agent memory in `.github/agents/memory/` for prior learnings
- Use semantic search for concept-based queries
- Use grep/file search for specific strings or patterns
- Keep files open in editor to provide implicit context

### Execution Best Practices
- Analyze request → check skills → plan with TODO tool → execute
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
- **Skills:** [list of skills from .github/skills/ that were referenced]
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
