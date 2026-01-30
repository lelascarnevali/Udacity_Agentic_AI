# Agent Memory Entry

- **Date:** 2026-01-29
- **Topic:** How to write agent memory entries (BMAD style)
- **Topics/Tags:** memory, conventions, bmad
- **Source:** repository documentation workflow

## Context
We need a clear, repeatable method for capturing agent learnings as Markdown entries under `.github/agents/memory`, ensuring consistency and usefulness across sessions and modules. Follow BMAD (Breakthrough Method of Agile AI Driven Development) conventions adapted to this repository.

## Decisions / Rules
- Use a simple, consistent structure with sections: Context, Key Insights, Decisions/Rules, References, Next Actions. Optional: Learned Patterns, Tags.
- Name files with `<context>-agent-memory.md` (kebab-case, no spaces). Include the date inside the entry, not in the filename.
- Keep entries concise, factual, and operational. Write for selective loading; avoid fluff.
- Prefer bullet points and headings. Reference exact paths and artifacts.

## Implementation
- Start new entries from `templates/learning-template.md`.
- Include concise metadata at the top (Date, Topic, Topics/Tags, Source).
- Populate sections with high-signal information:
  - Context: what changed and why it matters.
  - Key Insights: distilled lessons or findings.
  - Decisions/Rules: standards to apply and trade-offs considered.
  - References: internal paths and external links.
  - Next Actions: follow-ups to validate or extend.

## Techniques
- Write for engineers: be precise, minimal, and outcome-driven.
- Prefer bullet points; keep paragraphs short.
- Capture prompts/outcomes only if they illustrate a reusable pattern.
- Use tags to aid indexing and retrieval.

## References
- Memory conventions: `.github/agents/memory/README.md`.
- Template: `.github/agents/memory/templates/learning-template.md`.
- BMAD Method Home: https://docs.bmad-method.org/
- BMAD LLM-optimized doc: https://docs.bmad-method.org/llms-full.txt
- BMAD Agent Memory & Sidecar: https://deepwiki.com/bmad-code-org/BMAD-METHOD/7.4-agent-memory-and-sidecar-system

## Next Steps
- Apply this structure to future learnings in modules 2–4.
- Periodically synthesize memory entries into module `docs/` when patterns stabilize.
