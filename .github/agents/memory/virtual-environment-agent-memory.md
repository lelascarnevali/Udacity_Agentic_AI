# Agent Memory Entry

- **Date:** 2026-01-29
- **Topic:** Virtual environment usage in this repository
- **Topics/Tags:** environment, uv, virtualenv, jupyter
- **Source:** repository setup and usage

## Context
This repository standardizes Python environments via `uv` and a local `.venv` (Python 3.13). Notebooks are executed under the active virtual environment, and dependencies (including Jupyter) are installed using `uv pip` for speed and reproducibility.

## Key Insights
- Use a local `.venv` to isolate dependencies per project.
- Prefer `uv pip` over system `pip` to avoid global state and speed up installs.
- Keep secrets (e.g., `OPENAI_API_KEY`) in `.env` at repo root; do not hardcode in notebooks.
- Ensure Jupyter uses the active virtualenv to avoid kernel mismatches.

## Decisions / Rules
- Always activate `.venv` before running notebooks or scripts.
- Install and manage dependencies via `uv pip`; avoid global installs.
- Do not commit environment artifacts; only `.venv/` exists locally.
- Document environment steps in README and align examples to `uv` commands.
- Skills and helper scripts should be path-relative and not require global tooling.

## References
- README environment and quickstart sections.
- requirements.txt
- `.github/skills/agent-memory/SKILL.md`

## Next Actions
- Consider adding a small note in skill usage to run `new_memory_entry` with an active `.venv`.
- Periodically verify notebooks use the correct kernel (VS Code or Jupyter Lab).
- If VS Code Debugger launches `/opt/homebrew/bin/python3` instead of `.venv/bin/python`, add or update `.vscode/launch.json` with an explicit `"python"` path to the workspace virtualenv.
- If the editor's debug button still ignores `launch.json`, mark the configuration with `"purpose": ["debug-in-terminal"]` so the `Python Debugger: Debug Python File` command uses that launch config.
- For `debugpy` crashes on Python 3.14 with `'_MainThread' object has no attribute '_handle'`, set `PYDEVD_USE_SYS_MONITORING=0` in the debug configuration as a workspace workaround until the debugger extension is updated.
