---
applyTo: "**/*.py,**/requirements.txt,**/exercises/**/*.ipynb"
---

# Python Environment Instructions

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Teardown

```sh
deactivate
```

## Standards
- Follow PEP 8; prefer type hints and concise docstrings.
- Use `black` or `ruff` for formatting when applicable.
- Pin versions in `requirements.txt` for reproducibility.
- Prefer `.venv/` at workspace root; do not commit it to git.
