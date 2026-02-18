# Agent Memory Entry

- **Date:** 2026-02-18
- **Topic:** Mandatory memory check before task execution
- **Topics/Tags:** workflow, memory, agent-behavior, best-practices
- **Source:** User feedback on agent workflow improvement

## Context
Agent was not consulting existing memory entries in `.github/agents/memory/` before executing tasks. This causes:
1. **Duplication of work** (re-learning known patterns)
2. **Inconsistent outputs** (not following established preferences)
3. **Wasted context** (ignoring prior decisions and learnings)

User explicitly requested: "Você nunca está avaliando se tem memória para executar tarefa, corrija isso"

## Key Insights
- Memory entries contain **critical context** like style preferences, established workflows, and past decisions
- Reading memory **before** starting work enables consistency and efficiency
- The agent-memory skill exists specifically to create persistent learnings across sessions

## Decisions / Rules

### MANDATORY: Skill-First with Memory Context

**ALWAYS perform these steps before executing ANY task:**

1. **Identify relevant skill(s)** for the task type
2. **Read skill documentation** from `.github/skills/`
3. **Check for memory associated with that skill**:
   ```bash
   ls .github/agents/memory/
   # Look for: <skill-name>-agent-memory.md or related entries
   ```
4. **Read memory entries** that complement the skill
5. **Apply both**: skill workflow + memory learnings/preferences
6. **Update memory** after task if new patterns emerge

### Memory-to-Skill Mapping

| Skill | Associated Memory Files |
|:------|:-----------------------|
| `tech-writer` | `study-guide-preference.md` |
| `git-commit` | `terminal-troubleshooting.md` |
| `agent-memory` | `agent-memory-skill-usage-agent-memory.md`, `how-to-write-memory-agent-memory.md` |
| Python operations | `virtual-environment-agent-memory.md` |
| README creation | `readme-agent-memory.md` |
| General workflow | `workflow-memory-check-agent-memory.md` |

### Exception
Only skip memory check for **trivial conversational responses** that don't involve:
- File creation/editing
- Tool usage
- Multi-step workflows
- Documentation generation

## Implementation Pattern

```markdown
Before executing task:

1. 📚 CHECK SKILL:
   - Identify: relevant skill for task
   - Read: .github/skills/<skill-name>/SKILL.md
   - Understand: workflow and requirements

2. 🧠 CHECK MEMORY ASSOCIATED WITH SKILL:
   - List: .github/agents/memory/
   - Read: memory files linked to the skill
   - Apply: learnings/preferences/rules

3. 🔍 GATHER ADDITIONAL CONTEXT:
   - Semantic search (concepts)
   - Grep/file search (specific strings)
   - Existing files in editor

4. ⚙️ EXECUTE TASK:
   - Follow skill workflow
   - Apply memory guidelines
   - Maintain consistency

5. 💾 UPDATE MEMORY (if needed):
   - New patterns discovered?
   - Rules refined?
   - Create/update memory entry
```

## References
- Agent memory skill: `.github/skills/agent-memory/SKILL.md`
- Memory directory: `.github/agents/memory/`
- Memory template: `.github/skills/agent-memory/assets/templates/memory-template.md`

## Next Actions
- [ ] Update copilot-instructions.md to include mandatory memory check in workflow
- [ ] Verify all existing memory entries are properly named and structured
- [ ] Create memory checklist reminder for complex tasks

## Learned Patterns

### Good Practice Example:
```
User: "Crie um guia de estudo sobre X"
Agent: 
1. Identifies task → documentation creation
2. Checks skill → reads tech-writer/SKILL.md
3. Checks memory → reads study-guide-preference.md
4. Applies both: tech-writer structure + user preferences (emojis, tables, LaTeX, code-first)
5. Creates consistent output matching established patterns
```

### Bad Practice (to avoid):
```
User: "Crie um guia de estudo sobre X"
Agent:
1. Immediately starts creating doc (skips skill check)
2. Ignores memory preferences
3. Uses inconsistent structure
4. Forces user to request corrections
```

## Tags
#workflow #memory #mandatory #consistency #agent-behavior
