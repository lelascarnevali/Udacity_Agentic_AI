---
date: 2026-03-31
topic: architecture diagram and code alignment
topics: [mermaid, documentation, multi-agent, project-starter]
source: 4_Multi-Agent_Systems/project
---

# Agent Memory Entry

- **Date:** 2026-03-31
- **Topic:** Architecture diagram and code alignment
- **Topics/Tags:** Mermaid, documentation, multi-agent orchestration, tool registration
- **Source:** `4_Multi-Agent_Systems/project`

## Context
`architecture.mmd` needed to match the real tool registration in `project_starter.py` after reviewer feedback.

## Key Insights
- `supplier_delivery_tool()` belongs on the inventory side because it is registered on `InventoryAgent`.
- `financial_report_tool()` is shared by both `InventoryAgent` and `FulfillmentAgent`.
- When the code and diagram disagree, the reviewer will treat the mismatch as an architecture bug even if runtime behavior is correct.

## Decisions / Rules
- Keep Mermaid diagrams synchronized with the current tool registration map in code.
- Prefer updating the diagram to match the implementation when the implementation already reflects the intended design.

## References
- `4_Multi-Agent_Systems/project/architecture.mmd`
- `4_Multi-Agent_Systems/project/project_starter.py`
- Reviewer note about tool placement and reporting helpers

## Next Actions
- Recheck `architecture.svg` or other generated diagram outputs if they are part of the submission flow.
- Apply the same code-diagram sync rule to future agent architecture updates.

