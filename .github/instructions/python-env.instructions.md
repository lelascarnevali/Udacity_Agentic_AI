---
applyTo: "**/*.py,**/requirements.txt,**/exercises/**/*.ipynb"
---

# Python Environment Instructions

## Setup

To set up your Python environment, follow these steps:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Teardown

To deactivate your Python environment, use the following command:

```sh
deactivate
```

## Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/); prefer type hints and concise docstrings.
- Use `black` or `ruff` for formatting when applicable.
- Pin versions in `requirements.txt` for reproducibility.
- Prefer `.venv/` at the workspace root; do not commit it to git.

## Related Files

For more information on setting up your environment, refer to the [requirements.txt](requirements.txt) file for package dependencies and the [exercises](exercises/) directory for Jupyter Notebook examples.