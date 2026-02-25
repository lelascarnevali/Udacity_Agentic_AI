---
applyTo: ".github/**"
---

# Agent Workflow Architecture

This file defines **where each type of agent knowledge lives** in this repository.
When in doubt about where to put something, use this as the decision guide.

## Decision Table

| What you have | Where it goes | Format |
|---|---|---|
| Always-on project rules | `.github/copilot-instructions.md` | Free Markdown |
| Path-specific coding rules | `.github/instructions/*.instructions.md` | YAML frontmatter + Markdown |
| A repeatable task the user invokes | `.github/prompts/*.prompt.md` | YAML frontmatter + Markdown |
| A specialized AI persona / tool set | `.github/agents/*.agent.md` | YAML frontmatter + Markdown |
| A reusable procedure the AI loads automatically | `.github/skills/<name>/SKILL.md` | YAML frontmatter + Markdown |
| A learning / preference from a past session | `.github/agents/memory/*.md` | Free Markdown (memory template) |

## Detailed Roles

### 1. `copilot-instructions.md` → Always-On Project Context
- Summary of what the repo is, its stack, layout, critical rules
- Tool mapping (generic → VS Code / Claude Code)
- Read by Copilot on every request

### 2. `instructions/` → Scoped Coding Rules
- Applied automatically when Copilot works on matching files (`applyTo` glob)
- Examples: Python style rules, notebook conventions, module structure
- **Do NOT put workflows here** — instructions are guidelines, not step-by-step procedures

### 3. `prompts/` → User-Invoked Slash Commands
- Appear in the `/` menu in Copilot Chat
- Best for: complex multi-step workflows the user explicitly triggers
- Examples: `/documentation_workflow`, `/commit`
- **Key trait:** User decides when to run it

### 4. `agents/` → Specialized AI Personas
- Loaded when user selects the agent in the dropdown
- Controls which tools are available and the agent's behavior
- Best for: planning-only mode (read-only tools), implementation mode, review mode
- Examples: `plan.agent.md`
- **Key trait:** Changes the AI's available tools and persona

### 5. `skills/` → Auto-Loaded Reusable Procedures
- AI reads `name` + `description` on every request and loads the full SKILL.md when relevant
- Best for: how-to procedures the AI should follow automatically
- Examples: `git-commit`, `tech-writer`, `agent-memory`
- **Key trait:** AI decides when to load it based on task relevance

### 6. `agents/memory/` → Session Learnings
- Captures **what was learned** in past sessions, NOT primary procedure definitions
- Examples: user style preferences, discovered env quirks, past decisions
- **Rule:** If a memory file contains a primary workflow procedure, promote it to a Skill or Instruction

## Common Mistakes to Avoid

| ❌ Wrong | ✅ Right |
|---|---|
| Primary workflow in a memory file | Create a Skill or Instruction; reference it from memory |
| Always-on rule buried in a Skill | Move to `copilot-instructions.md` or `instructions/` |
| Slash command logic inside `copilot-instructions.md` | Create a `prompts/*.prompt.md` |
| Persona/tool restrictions in `copilot-instructions.md` | Create an `agents/*.agent.md` |
| Non-standard frontmatter (`license`, `allowed-tools`) in SKILL.md | Use only: `name`, `description`, `argument-hint`, `user-invokable`, `disable-model-invocation` |

## Current Workflow Split in This Repository

```
User types /documentation_workflow
  → prompts/documentation_workflow.prompt.md  (orchestrator)
      → skills/tech-writer/SKILL.md           (writing procedure)
      → skills/agent-memory/SKILL.md          (memory logging)
      → agents/memory/study-guide-preference.md (style preferences)

User selects @Plan agent
  → agents/plan.agent.md                      (read-only persona)
      → skills/README.md                      (skill catalog)
      → agents/memory/README.md               (memory index)

User types /commit
  → prompts/commit.prompt.md                  (orchestrator)
      → skills/git-commit/SKILL.md            (commit procedure)
      → agents/memory/terminal-troubleshooting.md (known quirks)
```

## Adding a New Workflow — Checklist

- [ ] Is it user-invoked? → `prompts/`
- [ ] Is it a persona with tool restrictions? → `agents/`
- [ ] Is it a procedure the AI loads automatically? → `skills/`
- [ ] Is it a learning from this session? → `agents/memory/`
- [ ] Does it apply to all files always? → `copilot-instructions.md`
- [ ] Does it apply to specific file types? → `instructions/`
