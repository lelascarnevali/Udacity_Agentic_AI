# GitHub Copilot — Tool Adapter

> All project instructions are in [`AGENTS.md`](../AGENTS.md). Read that file **before** planning or executing any task.
> This file only defines the GitHub Copilot / VS Code-specific tool mappings referenced in `AGENTS.md`.

## Tool Mapping

When `AGENTS.md` refers to generic AI assistant tools, use the following VS Code / Copilot equivalents:

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

Skills are integrated via the shell script at `.github/skills/`. See `.github/skills/README.md` for the catalog.
