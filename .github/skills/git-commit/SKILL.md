---
name: git-commit
description: Automate git commits using Conventional Commits. Trigger phrases: "commit changes", "create a git commit", "use /commit". Use when needing to auto-detect commit type/scope, generate messages from diffs, and intelligently stage files.
argument-hint: '[type] [scope] [description] — or leave empty for auto-detection'
---

# Git Commit with Conventional Commits

## Overview

This skill helps you create standardized, semantic git commits using the Conventional Commits specification. It analyzes the diff to determine the appropriate type, scope, and message for your commit.

## Workflow

### 1. Analyze Diff

1. Run `git status --porcelain` to check the current status.
2. If files are staged, use `git diff --staged` to read the full staged diff.
3. If nothing is staged, use `git diff` to read the working tree diff.

> Ensure the commit message is derived from the actual diff output.

### 2. Stage Files

If you need to stage files:

1. Use `git add path/to/file1 path/to/file2` to stage specific files.
2. Use `git add *.test.*` or `git add src/components/*` to stage by pattern.
3. Use `git add -p` for interactive staging.

> Avoid committing sensitive files like `.env` or `credentials.json`.

### 3. Generate Commit Message

1. Determine the **Type**: What kind of change is this?
2. Determine the **Scope**: What area/module is affected?
3. Write a **Description**: A one-line summary of what changed.

> Derive type, scope, and description directly from the diff content.

### 4. Execute Commit

1. For a single line commit: `git commit -m "<type>[scope]: <description>"`
2. For multi-line commit with body/footer:

```bash
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<optional body>

<optional footer>
EOF
)"
```

## Best Practices

- Commit one logical change at a time.
- Use present tense and imperative mood.
- Reference issues with `Closes #123` or `Refs #456`.
- Keep descriptions under 72 characters.

## Git Safety Protocol

- Avoid updating git config or running destructive commands without explicit request.
- Do not skip hooks unless requested.
- Avoid force pushing to main/master.
- If a commit fails due to hooks, fix the issue and create a new commit.

## Troubleshooting

1. **Commit message rejected by hooks**: Review the error message, fix the issues, and create a new commit.
2. **Staging errors**: Verify the staging area with `git status` and stage files as needed.
3. **Incorrect commit message format**: Ensure the message follows the Conventional Commits specification.
4. **Unstaged changes**: Use `git status` to ensure all intended changes are staged.

## Example

### Input

User says: "commit changes with type 'fix', scope 'auth', description 'resolve login issue'"

### Output

```bash
git commit -m "fix(auth): resolve login issue"
```

For detailed information on commit types and breaking changes, refer to the [Conventional Commits Reference](reference/conventional-commits.md).