# Skills Catalog

This directory contains specialized skills that extend Copilot's capabilities with domain-specific knowledge, workflows, and tools.

## 📋 Quick Reference

**Always check this catalog before executing tasks** - skills provide validated, tested procedures that should be used instead of direct commands.

## 🛠️ Available Skills


### `agent-memory`

**Description:** Agent memory logging for engineering learnings using Markdown entries.

**Location:** [.github/skills/agent-memory/](.github/skills/agent-memory/)


### `crafting-effective-readmes`

**Description:** Use when writing or improving README files. Not all READMEs are the same — provides templates and guidance matched to your audience and project type.

**Location:** [.github/skills/crafting-effective-readmes/](.github/skills/crafting-effective-readmes/)


### `find-skills`

**Description:** Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.

**Location:** [.github/skills/find-skills/](.github/skills/find-skills/)


### `git-commit`

**Description:** Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "/commit". Supports: (1) Auto-detecting type and scope from changes, (2) Generating conventional commit messages from diff, (3) Interactive commit with optional type/scope/description overrides, (4) Intelligent file staging for logical grouping

**Location:** [.github/skills/git-commit/](.github/skills/git-commit/)


### `skill-catalog-updater`

**Description:** Automatically updates the skills catalog (README.md) when skills are created or deleted. Scans .github/skills/ directory, extracts metadata from SKILL.md files, and regenerates the catalog with consistent formatting.

**Location:** [.github/skills/skill-catalog-updater/](.github/skills/skill-catalog-updater/)


### `skill-creator`

**Description:** Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

**Location:** [.github/skills/skill-creator/](.github/skills/skill-creator/)


---

## 🚀 Usage Workflow

1. **Check this catalog** before starting any task
2. **Search for relevant skill** using semantic search or keywords
3. **Read the skill's SKILL.md** for detailed instructions
4. **Follow the skill's workflow** instead of using direct commands
5. **Trust the skill** - they contain validated, tested procedures

## 🔄 Keeping This Catalog Updated

This catalog is **automatically maintained** by the `skill-catalog-updater` skill.

**To update:** Run `.github/skills/skill-catalog-updater/update-catalog.sh`

---

*Last updated: 2026-02-09 23:03:58*
