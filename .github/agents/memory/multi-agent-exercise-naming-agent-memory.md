# Agent Memory Entry

- **Date:** 2026-03-26
- **Topic:** Multi-agent exercise file naming
- **Topics/Tags:** exercises, naming, multi-agent-systems, demo
- **Source:** repository renaming workflow for exercises 02-05

## Context
We aligned the multi-agent exercise folders so the main exercise file and the demo file use the parent folder name instead of generic names like `starter.py` or `demo.py` across modules 02 through 07.

## Key Insights
- The consistent pattern is `exercise/<folder-name>.py` or `exercises/<folder-name>.py` and `demo/<folder-name>-demo.py`.
- This applies across the 01-05 multi-agent exercise set.
- The 05 state-management, 06 state-coordination, and 07 RAG modules keep their existing directory layout, but the file naming still follows the folder-name pattern.

## Decisions / Rules
- Prefer folder-derived filenames for exercise scaffolding to make navigation predictable.
- Update any README references that still mention the old generic filenames.

## References
- `4_Multi-Agent_Systems/exercises/02-multi-agent-architecture-implementation/exercises/2-multi-agent-architecture-implementation.py`
- `4_Multi-Agent_Systems/exercises/02-multi-agent-architecture-implementation/demo/2-multi-agent-architecture-implementation-demo.py`
- `4_Multi-Agent_Systems/exercises/04-routing-and-data-flow-in-agentic-systems/exercises/04-routing-and-data-flow-in-agentic-systems.py`
- `4_Multi-Agent_Systems/exercises/04-routing-and-data-flow-in-agentic-systems/demo/04-routing-and-data-flow-in-agentic-systems-demo.py`
- `4_Multi-Agent_Systems/exercises/05-state-management-in-multi-agent-systems/exercise/05-state-management-in-multi-agent-systems.py`
- `4_Multi-Agent_Systems/exercises/05-state-management-in-multi-agent-systems/demo/05-state-management-in-multi-agent-systems-demo.py`
- `4_Multi-Agent_Systems/exercises/06-multi-agent-state-coordination-and-orchestration/exercise/06-multi-agent-state-coordination-and-orchestration.py`
- `4_Multi-Agent_Systems/exercises/06-multi-agent-state-coordination-and-orchestration/demo/06-multi-agent-state-coordination-and-orchestration-demo.py`
- `4_Multi-Agent_Systems/exercises/07-multi-agent-retrieval-augmented-generation/exercise/07-multi-agent-retrieval-augmented-generation.py`
- `4_Multi-Agent_Systems/exercises/07-multi-agent-retrieval-augmented-generation/demo/07-multi-agent-retrieval-augmented-generation-demo.py`

## Next Actions
- Reuse this naming pattern when touching later multi-agent exercise folders.

## Learned Patterns (optional)
- Folder name drives file name; demo files reuse the same base with `-demo`.

## Tags (optional)
multi-agent, exercises, naming, documentation
