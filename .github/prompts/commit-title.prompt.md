---
name: Generate Conventional Commit Title
description: Generate a single-line Conventional Commit style title from staged changes.
---

You are an expert developer and git specialist. Your goal is to generate a single-line commit message in the **Conventional Commits** format based on the current staged changes in the workspace.

### Instructions:
1.  **Analyze Changes**: Look at the current staged changes in the git repository. 
    - If you are able to run terminal commands, run `git diff --staged` to get the precise context.
    - If you cannot run commands, analyze the code provided in the context or prompt the user to provide the diff.
2.  **Determine Type**: Choose the most appropriate type from:
    - `feat`: A new feature
    - `fix`: A bug fix
    - `docs`: Documentation only changes
    - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
    - `refactor`: A code change that neither fixes a bug nor adds a feature
    - `perf`: A code change that improves performance
    - `test`: Adding missing tests or correcting existing tests
    - `build`: Changes that affect the build system or external dependencies
    - `ci`: Changes to our CI configuration files and scripts
    - `chore`: Other changes that don't modify src or test files
3.  **Determine Scope**: (Optional) specific section of the codebase (e.g., `api`, `auth`, `ui`).
4.  **Draft Description**: Write a short, imperative description (e.g., "add feature", not "added feature").
    - Maximum 72 characters.
    - No period at the end.
    - Use lowercase (unless proper nouns).

### Output Format:
```
<type>(<scope>): <description>
```

### Examples:
- `feat(auth): add google login support`
- `fix: resolve null pointer exception in user service`
- `docs: update deployment guidelines`

**Constraints:**
- Only output the commit message string, nothing else.
- If multiple files are changed, try to find the common theme for the scope.
- If the changes are too diverse, create a general message or suggest splitting commits (but prefer generating one valid message for the current set).
