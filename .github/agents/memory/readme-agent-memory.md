# Agent Memory Entry

- **Date:** 2026-01-29
- **Topic:** README scope and agent memory location

## Context
The repository README was refined to stay focused on purpose, setup, usage, and structure. Agent learnings should not be documented in README; they belong in `.github/agents/memory` as Markdown entries.

## Decisions
- Keep programming standards and Copilot instructions out of README to prevent duplication and drift.
- Establish `.github/agents/memory` as the persistent store for learnings, with `.gitignore` allowing only `.md` files.
- Use a template for consistent entries and date-based naming.

## Implementation
- Created `.github/agents/memory/templates/learning-template.md` for standardized entries.
- Added `.github/agents/memory/.gitignore` to ignore non-markdown artifacts while tracking `.md` and `.gitkeep`.
- Placed this entry under date-based naming.

## Techniques
- Documentation decoupling: separate usage docs (README) from agent memory logs.
- Minimal, high-signal notes tailored for engineers.

## References
- Memory conventions: see `.github/agents/memory/README.md`.
- Copilot instructions: `.github/copilot-instructions.md`.

## Do not include
- Code dumps or extensive programming standards.

## Next Steps
- Record future learnings per module (2–4) using the template.
- Revisit memory entries to synthesize design decisions into module docs when stable.
