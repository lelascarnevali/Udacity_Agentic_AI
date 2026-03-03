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


### `git-commit`

**Description:** Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "/commit". Supports: (1) Auto-detecting type and scope from changes, (2) Generating conventional commit messages from diff, (3) Interactive commit with optional type/scope/description overrides, (4) Intelligent file staging for logical grouping

**Location:** [.github/skills/git-commit/](.github/skills/git-commit/)


### `mermaid-diagrams`

**Description:** Comprehensive guide for creating software diagrams using Mermaid syntax. Use when users need to create, visualize, or document software through diagrams including class diagrams (domain modeling, object-oriented design), sequence diagrams (application flows, API interactions, code execution), flowcharts (processes, algorithms, user journeys), entity relationship diagrams (database schemas), C4 architecture diagrams (system context, containers, components), state diagrams, git graphs, pie charts, gantt charts, or any other diagram type. Triggers include requests to "diagram", "visualize", "model", "map out", "show the flow", or when explaining system architecture, database design, code structure, or user/application flows.

**Location:** [.github/skills/mermaid-diagrams/](.github/skills/mermaid-diagrams/)


### `prompt-engineering`

**Description:** Use this skill when you writing commands, hooks, skills for Agent, or prompts for sub agents or any other LLM interaction, including optimizing prompts, improving LLM outputs, or designing production prompt templates.

**Location:** [.github/skills/prompt-engineering/](.github/skills/prompt-engineering/)


### `skill-creator`

**Description:** Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

**Location:** [.github/skills/skill-creator/](.github/skills/skill-creator/)


### `tech-writer`

**Description:** Apply rigorous technical writing standards (Strunk & White) to create or update documentation. Use for creating study guides, cheat sheets, or updating project docs based on local code changes.

**Location:** [.github/skills/tech-writer/](.github/skills/tech-writer/)


---

## 🚀 Usage Workflow

1. **Check this catalog** before starting any task
2. **Search for relevant skill** using semantic search or keywords
3. **Read the skill's SKILL.md** for detailed instructions
4. **Follow the skill's workflow** instead of using direct commands
5. **Trust the skill** - they contain validated, tested procedures

## 🔄 Keeping This Catalog Updated

This catalog is **automatically maintained** by the catalog updater utility.

**To update:** Run `.github/skills/skill-creator/catalog-updater/update-catalog.sh`

This is integrated into the `skill-creator` workflow - see that skill for details.

---

*Last updated: 2026-03-02 21:52:00*
