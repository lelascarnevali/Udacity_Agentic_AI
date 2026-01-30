# Agent Memory Entry

- **Date:** 2026-01-29
- **Topic:** How to write agent memory entries

## Context
We need a clear, repeatable method for capturing agent learnings as Markdown entries under `.github/agents/memory`, ensuring consistency and usefulness across sessions and modules.

## Decisions
- Use a simple, consistent structure with sections: Context, Decisions, Implementation, Techniques, References, Next Steps.
- Name files with `YYYY-MM-DD-<topic>.md` to keep chronological order and searchability.
- Avoid code dumps; focus on engineering insights, rationale, and actionable next steps.

## Implementation
- Start new entries from `templates/learning-template.md`.
- Include a concise title and date at the top.
- Populate each section with high-signal information:
  - Context: what changed and why it matters.
  - Decisions: choices made and trade-offs.
  - Implementation: artifacts created/updated and locations.
  - Techniques: prompting/workflow patterns and reasoning strategies.
  - References: links to docs or specs.
  - Next Steps: follow-ups to validate or extend.

## Techniques
- Write for engineers: be precise, minimal, and outcome-driven.
- Prefer bullet points; keep paragraphs short.
- Capture prompts and outcomes only if they illustrate a reusable pattern.

## References
- Memory conventions: `.github/agents/memory/README.md`.
- Template: `.github/agents/memory/templates/learning-template.md`.

## Next Steps
- Apply this structure to future learnings in modules 2–4.
- Periodically synthesize memory entries into module `docs/` when patterns stabilize.
