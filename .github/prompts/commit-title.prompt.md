---
title: Generate Conventional Commit Title
description: Generate a single-line Conventional Commit style title for a PR.
tags: [commit, conventional-commit, commit-message]
author: repo-automation
---

You are GitHub Copilot. Given the pull request title, body, author and list of changed files, generate exactly one commit message in Conventional Commits format.

Rules:
- Choose one type from: feat, fix, docs, chore, refactor, test, perf.
- Prefer the type based on PR title/body/files (code changes → feat/fix/refactor; docs → docs).
- If an obvious scope exists (module/file/folder), include it as `type(scope): short-description`.
- Keep the short description ≤72 characters, imperative and concise.
- Use present-tense, imperative verbs (e.g., "Add", "Fix", "Update").
- Output only the single commit message line in English.

Input placeholders (replace with PR data):
PR_TITLE: {PR_TITLE}
PR_BODY: {PR_BODY}
PR_AUTHOR: {PR_AUTHOR}
CHANGED_FILES: {CHANGED_FILES}

Now generate the commit message.
