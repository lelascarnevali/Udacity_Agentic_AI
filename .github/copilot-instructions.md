# GitHub Copilot Instructions

This repository hosts Udacity Agentic AI exercises focused on effective prompting for LLM reasoning and planning. Keep guidance minimal, precise, and aligned with the actual workspace.

## 1. Repository Context
- Purpose: hands-on notebooks and lightweight utilities for LLM reasoning and planning.
- Stack: macOS + VS Code + Jupyter + Python.

## 2. Repository Structure
```
.
├── .github/
│   ├── copilot-instructions.md       # This file
│   └── skills/                       # Copilot skills    
├── 1_Prompting_for_Effective_LLM_Reasoning_and_Planning/ # Module 1 of this course
│   ├── docs/                         # Course content and references
│   └── exercises/                    # Exercise notebooks
├── scripts/                          # Reusable Python utilities for notebooks
├── .github/
│   ├── copilot-instructions.md       # This file
├── .venv/                            # Local Python virtual environment (optional)
├── README.md                         # Project overview and how to run
├── requirements.txt                  # Project dependencies
└── .gitignore                        # Git ignore rules
```

## 3. Skills (skill.sh)
- integrate Copilot "skills" via a shell script.
- Skills location: `.github/skills/`.


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

— End of instructions —
