---
name: agent-memory
description: Captures persistent agent learnings using Markdown entries for future reference. Use this skill when completing a task to log reusable lessons or workflow discoveries. Trigger phrases include 'log my task learnings' or 'record workflow insights'.
argument-hint: '[context/topic] — e.g. "virtualenv setup" or "study-guide preferences"'
---

# Agent Memory

This skill standardizes capturing persistent agent learnings using a concise, consistent memory format.

## When to Use
- After completing a task, design decision, or investigation with lessons worth retaining.
- When you need reproducible, loadable notes for agents across sessions.
- To keep README focused on setup/usage while memory lives separately.

## Location & Naming
- Memory root: `.github/agents/memory/`
- Filename pattern: `<context>-agent-memory.md` (kebab-case; no spaces)
- Date: include inside the entry body, not in the filename

## Template
Start from the memory template:
- Path: `.github/skills/agent-memory/assets/templates/memory-template.md`
- Copy to `.github/agents/memory/<context>-agent-memory.md`

## Structure
- Metadata (top): Date, Topic, Topics/Tags, Source
- Context: what changed and why it matters
- Key Insights: distilled lessons/findings
- Decisions/Rules: standards and trade-offs
- References: internal paths and external links
- Next Actions: follow-ups to validate or extend
- Optional: Learned Patterns, Tags

## Instructions
1. Identify the context/topic for your memory entry (e.g., "virtualenv setup").
2. Navigate to the memory template at `.github/skills/agent-memory/assets/templates/memory-template.md`.
3. Copy the template to `.github/agents/memory/<context>-agent-memory.md`.
4. Fill in the template sections with relevant information:
   - Metadata: Include date, topic, and tags.
   - Context: Describe changes and their significance.
   - Key Insights: Summarize lessons learned.
   - Decisions/Rules: Note any standards or trade-offs.
   - References: List internal and external resources.
   - Next Actions: Outline any follow-up tasks.
5. Save the file and ensure it is tracked in `.github/agents/memory/.gitignore`.

### Example
**Input:** Context: "virtualenv setup", Date: "2023-10-01", Key Insights: "Using virtualenv simplifies dependency management."

**Output:** A new file named `virtualenv-setup-agent-memory.md` containing:
```
Date: 2023-10-01
Topic: virtualenv setup
Tags: python, environment
Source: Internal project setup
Context: Implemented virtualenv to manage dependencies, reducing conflicts.
Key Insights: Using virtualenv simplifies dependency management.
Decisions/Rules: Adopt virtualenv for all Python projects.
References: [virtualenv documentation](https://virtualenv.pypa.io/en/latest/)
Next Actions: Train team on virtualenv usage.
```

## Quick Create (macOS/Linux)
```bash
# From repo root
ctx="role-based-prompting"
.github/skills/agent-memory/scripts/new_memory_entry "${ctx}"
```

## Conventions
- Keep entries concise, factual, and operational; prefer bullets.
- Reference exact files/paths; avoid code dumps.
- Do not duplicate programming standards or Copilot instructions here.
- `.github/agents/memory/.gitignore` tracks only `.md` and `.gitkeep`.

## Maintenance (MANDATORY)
After creating a new memory file, you **MUST** update the index at `.github/agents/memory/README.md`.
- Add a new row to the table.
- **Context/Skill**: The skill or context associated with the memory.
- **Relevant Memory File**: Link to the new file (e.g., `[my-new-memory.md](my-new-memory.md)`).
- **Description**: A brief summary of what the memory contains.

## Troubleshooting
- **Error: File not found**: Ensure the template path is correct and the file exists. Verify the path `.github/skills/agent-memory/assets/templates/memory-template.md`.
- **Error: Permission denied**: Check file permissions and ensure you have write access to the destination directory.
- **Output not as expected**: Verify that all sections of the template are filled out correctly. Ensure metadata, context, and insights are complete.
- **Template not copied**: Confirm the destination path `.github/agents/memory/<context>-agent-memory.md` is correct and writable. Check for typos in the context name.

## References
- Memory conventions: `.github/agents/memory/README.md`
- Template: `.github/skills/agent-memory/assets/templates/memory-template.md`
---