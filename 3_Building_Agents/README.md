# Udacity Project — UdaPlay: AI Game Research Agent

## Project: Building an Intelligent Agent for Video Game Research

### Project Introduction

Building a functional AI agent requires more than wiring an LLM to a chat loop —
it demands tools, memory, structured state, and the ability to reason across multiple
retrieval strategies. This project applies that full stack to a concrete domain:
video game research.

In this project, I build **UdaPlay**, an AI-powered research agent for the video game
industry. The agent answers questions about games using a local vector knowledge base
(offline RAG) and falls back to live web search when the local data is insufficient.
It maintains conversation history across turns and returns structured, verifiable outputs.

---

### Project Summary

The solution is delivered in two parts:

#### Part 1: Offline RAG — Vector Knowledge Base

A ChromaDB-backed vector store indexing 15 video game records. Each game document
contains: Name, Platform, Genre, Publisher, Description, and Year of Release.

Key tasks:
- Set up ChromaDB as a persistent client with OpenAI embeddings (`text-embedding-3-small`)
- Create a collection and process game data from JSON files
- Implement `retrieve_game` tool — semantic search against the local collection
- Implement `evaluate_retrieval` tool — assess whether retrieved results are relevant

#### Part 2: AI Agent with Tools and Memory

An intelligent agent that orchestrates local RAG and web search via a state machine
workflow. The agent decides *when* to use which tool, maintains conversation state
across turns, and stores useful information for future sessions.

Required tools implemented:

| Tool | Purpose |
|------|---------|
| `retrieve_game` | Semantic search in the ChromaDB vector store |
| `evaluate_retrieval` | Assess the quality and relevance of retrieved results |
| `game_web_search` | Perform Tavily-powered web search for real-time information |

---

### Architecture Overview

```
user_query
      │
      ▼
EntryPoint
      │
      ▼
message_prep  ──── inject SystemMessage + UserMessage ──▶  messages[]
      │
      ▼
llm_processor  ──── LLM.invoke(messages) ──▶  AIMessage + optional tool_calls
      │
      ├─▶ [tool_calls present] ──▶  tool_executor ──── execute tools ──▶  ToolMessages[]
      │                                   │
      │                                   └─▶ [loop back to llm_processor]
      │
      └─▶ [no tool_calls]  ──▶  web_search ──── web_search tool ──▶  UserMessage
      │
      ▼
comparison  ──── LLM compares agent answer vs. web results ──▶  comparison
      │
      ▼
Termination
```

The conditional edge after `llm_processor` implements the **tool-use loop**: if
the model requests tool calls, the executor handles them and returns control to
the LLM for a second pass. Once the LLM produces a final answer, the agent
cross-references it against a live web search and records a comparison.

---

## Project Evaluation Key Points

### Part 1 — Offline RAG

**ChromaDB Setup**
- `VectorStoreManager` initialized with `text-embedding-3-small` embedding function.
- Persistent ChromaDB client created and collection configured.
- 15 game JSON files processed and indexed as `Document` objects in the vector store.

**Tools**
- `retrieve_game`: Queries the vector store via semantic similarity; returns top-k
  game records matching the natural-language query.
- `evaluate_retrieval`: Applies an LLM judge (or heuristic) to decide whether the
  retrieved results are sufficient to answer the question.

### Part 2 — AI Agent

**Agent State Machine (`agents.py`)**
- `AgentState` (TypedDict) tracks: `user_query`, `instructions`, `messages`,
  `current_tool_calls`, `comparison`, and `session_id`.
- Six steps wired via `StateMachine`: `entry → message_prep → llm_processor →
  [tool_executor | web_search] → comparison → termination`.
- Conditional edge routes to `tool_executor` when `current_tool_calls` is non-empty,
  otherwise to `web_search`.

**Memory**
- `ShortTermMemory`: Session-based in-memory store; deep-copies each `Run` object
  to prevent state mutation across turns. Previous messages are loaded at the start
  of each `invoke` call.
- `LongTermMemory` (advanced): Vector-backed persistent store using ChromaDB for
  user preferences and facts that survive across sessions.

**Structured Output**
- Agent produces a final answer plus a `comparison` field that contrasts its
  knowledge-base response against the web search result for verifiability.

---

### Directory Structure

```
3_Building_Agents/
├── README.md                             ← This file
├── docs/                                 ← Study guides (Portuguese)
│   ├── 01-extending-agents-with-tools.md
│   ├── 02-structured-outputs.md
│   ├── 03-agent-state-management.md
│   ├── 04-short-term-memory.md
│   ├── 05-external-apis-and-tools.md
│   ├── 06-web-search-agents.md
│   ├── 07-interacting-with-databases.md
│   ├── 08-agentic-rag.md
│   ├── 09-long-term-memory.md
│   ├── 10-agentic-evaluation.md
│   └── README.md
├── exercises/                            ← Course exercises (Jupyter notebooks)
│   ├── 01-tool-calling-demo.ipynb
│   ├── 01-tool-calling-exercise.ipynb
│   ├── 02-structured-outputs-demo.ipynb
│   ├── 02-structured-outputs-exercise.ipynb
│   ├── 03-state-machine-demo.ipynb
│   ├── 03-state-machine-exercise.ipynb
│   ├── 04-short-term-memory-demo.ipynb
│   ├── 04-short-term-memory-exercise.ipynb
│   ├── 05-external-apis-demo.ipynb
│   ├── 05-external-apis-exercise.ipynb
│   ├── 06-web-search-exercise.ipynb
│   ├── 07-interacting-databases-demo.ipynb
│   ├── 08-agentic-rag-demo.ipynb
│   ├── 08-agentic-rag-exercise.ipynb
│   ├── 09-long-term-memory-demo.ipynb
│   ├── 10-agentic-evaluation-demo.ipynb
│   ├── pdf/                              ← Documents for RAG exercises
│   │   ├── GlobalEVOutlook2025.pdf
│   │   └── TheGamingIndustry2024.pdf
│   └── lib/                             ← Shared library for exercises
│       ├── agents.py                    ← Agent + AgentState
│       ├── state_machine.py             ← StateMachine, Step, Run, Snapshot
│       ├── memory.py                    ← ShortTermMemory + LongTermMemory
│       ├── documents.py                 ← Document, Corpus
│       ├── llm.py                       ← LLM abstraction
│       ├── messages.py                  ← AIMessage, UserMessage, ToolMessage
│       ├── tooling.py                   ← Tool adapter + @tool decorator
│       ├── parsers.py                   ← Output parsers
│       ├── rag.py                       ← RAG utilities
│       ├── loaders.py                   ← PDFLoader
│       ├── vector_db.py                 ← VectorStore, VectorStoreManager
│       └── evaluation.py               ← Evaluation utilities
└── project/
    ├── README.md
    ├── Udaplay_01_starter_project.ipynb  ← Part 1: ChromaDB + RAG setup
    ├── Udaplay_02_starter_project.ipynb  ← Part 2: Agent implementation
    ├── games/                           ← 15 JSON game records (input data)
    │   ├── 001.json … 015.json
    ├── chromadb/                        ← Persistent ChromaDB storage
    └── lib/                             ← Project library (mirrors exercises/lib)
```

---

## Solution

> **Instructor Note:** This section explains the reference solution for the
> UdaPlay project. Read it after you have attempted the implementation on your
> own. Understanding *why* each design decision was made is as important as
> making the code run.

### Reference Files

| Part | File | Description |
|------|------|-------------|
| Part 1 | [Udaplay_01_starter_project.ipynb](./project/Udaplay_01_starter_project.ipynb) | ChromaDB setup + RAG tool implementation |
| Part 2 | [Udaplay_02_starter_project.ipynb](./project/Udaplay_02_starter_project.ipynb) | Agent implementation with tools and memory |
| Library | [project/lib/](./project/lib/) | Full shared library (agents, state machine, memory, tools) |
| Data | [project/games/](./project/games/) | 15 game JSON files used as the knowledge base |

---

### Workflow

1. **Vector Store Setup (Part 1):**
   A `VectorStoreManager` initializes a ChromaDB client with the
   `text-embedding-3-small` embedding function. Each of the 15 game JSON files
   is loaded as a `Document` and indexed into a named collection. The store
   becomes the agent's "local brain" for offline queries.

2. **Tool Implementation (Part 1 → Part 2):**
   `retrieve_game` translates a natural-language question into a vector query
   and returns the top-k matching game records. `evaluate_retrieval` then applies
   an LLM judge to determine whether those results are sufficient. `game_web_search`
   calls Tavily when the local store cannot answer.

3. **State Machine Orchestration (Part 2):**
   The `Agent` class builds a `StateMachine[AgentState]` with six wired steps.
   On each `invoke` call it loads prior messages from `ShortTermMemory`, builds
   the initial state, and runs the machine until `Termination`.

4. **Tool-Use Loop (Part 2):**
   After `llm_processor` runs, a conditional transition checks `current_tool_calls`.
   If the LLM requested tools, `tool_executor` dispatches each call and loops back
   to `llm_processor` with the tool results appended as `ToolMessage` objects.
   This cycle continues until the model produces a final answer without tool calls.

5. **Web Search + Comparison (Part 2):**
   After the tool-use loop resolves, `web_search` performs an unconditional
   Tavily search for the original user query and appends the result as a
   `UserMessage`. The `comparison` step then asks the LLM to briefly contrast
   its answer against the web results, surfacing any discrepancies.

---

### Key Design Decisions

#### 1. State Machine as the Agent's Skeleton

Rather than a bare `while True` loop, the agent uses a typed `StateMachine` with
explicit `Step` nodes and `Transition` edges. Every step's output is captured in
a `Snapshot`, producing a full `Run` object — a complete, auditable execution
history.

**Why it matters:** When an agent behaves unexpectedly, you can replay its exact
step-by-step state changes. The separation between step logic and orchestration
also makes each node independently testable.

#### 2. `AgentState` as the Single Source of Truth

All data flows through a single `TypedDict` — `AgentState`. Steps receive the
full state and return only the fields they mutate. No implicit global state, no
closure-captured variables.

**Lesson:** This pattern, inspired by LangGraph, makes it trivial to add a new
step without refactoring existing ones. Each step is a pure function on the state.

#### 3. `ShortTermMemory` Stores `Run` Objects, Not Raw Messages

Short-term memory persists the entire `Run` from the previous turn. On the next
`invoke`, the agent fetches the `Run`'s final state and extracts its `messages`
list for continuity. This preserves the full conversation history without
additional serialization.

**Why it matters:** Storing structured `Run` objects (rather than flat strings)
means introspection tooling can retrospectively audit any prior turn.

#### 4. Tool-Use Loop vs. Single-Pass

The transition from `llm_processor` back to itself (via `tool_executor`) implements
a **multi-turn tool-use loop**: the LLM can call several tools in sequence across
multiple internal iterations before producing its final answer. The loop terminates
naturally when `current_tool_calls` is `None`.

**Lesson:** A single LLM call is rarely enough for tool-using agents. The loop
pattern handles chains like: retrieve → evaluate → web search → synthesize.

#### 5. Web Search as a Grounding Layer, Not a Fallback

The `web_search` step runs *unconditionally* after every final LLM answer, not
only when local retrieval fails. The `comparison` step then flags any divergence
between the agent's initial response and live web evidence.

**Why it matters:** This turns the web search into an automated fact-checking
layer, surfacing knowledge cutoff issues or hallucinations without requiring the
user to ask a follow-up question.

#### 6. `Tool` Adapter and `@tool` Decorator

The `Tool` class infers a compact JSON schema directly from Python type hints and
docstrings. Functions decorated with `@tool` are automatically available for
LLM function-calling without manually writing OpenAI tool schemas.

**Lesson:** Keeping the schema co-located with the implementation (via type hints)
reduces drift between what the code does and what the model is told it can do.

---

### Key Technologies

| Technology | Purpose |
|-----------|---------|
| OpenAI `gpt-4o-mini` (or similar) | Chat completions for agent responses and evaluation |
| OpenAI `text-embedding-3-small` | Embedding generation for vector search |
| ChromaDB | Persistent vector store for game knowledge base and long-term memory |
| Tavily API | Live web search for real-time information retrieval |
| `python-dotenv` | API key management via `.env` files |
| `pydantic` | Structured output parsing and validation |
| `pypdf` | PDF loading for RAG exercises |

---

### Exercises (Learning Path)

The notebooks below build the skills applied in the project:

| # | Notebooks | Topic |
|---|-----------|-------|
| 01 | [Demo](./exercises/01-tool-calling-demo.ipynb) · [Exercise](./exercises/01-tool-calling-exercise.ipynb) | Tool calling with function schemas |
| 02 | [Demo](./exercises/02-structured-outputs-demo.ipynb) · [Exercise](./exercises/02-structured-outputs-exercise.ipynb) | Structured outputs with Pydantic |
| 03 | [Demo](./exercises/03-state-machine-demo.ipynb) · [Exercise](./exercises/03-state-machine-exercise.ipynb) | State machine orchestration |
| 04 | [Demo](./exercises/04-short-term-memory-demo.ipynb) · [Exercise](./exercises/04-short-term-memory-exercise.ipynb) | Short-term memory across turns |
| 05 | [Demo](./exercises/05-external-apis-demo.ipynb) · [Exercise](./exercises/05-external-apis-exercise.ipynb) | External APIs and tools |
| 06 | [Exercise](./exercises/06-web-search-exercise.ipynb) | Web search agents with Tavily |
| 07 | [Demo](./exercises/07-interacting-databases-demo.ipynb) | Interacting with SQL databases |
| 08 | [Demo](./exercises/08-agentic-rag-demo.ipynb) · [Exercise](./exercises/08-agentic-rag-exercise.ipynb) | Agentic RAG with retrieve-reflect-retry |
| 09 | [Demo](./exercises/09-long-term-memory-demo.ipynb) | Long-term memory with vector stores |
| 10 | [Demo](./exercises/10-agentic-evaluation-demo.ipynb) | Agentic evaluation with LLM-as-judge |

---

### References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Tavily API](https://tavily.com/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [LangGraph: State Machines for Agents](https://langchain-ai.github.io/langgraph/)
- [Agentic RAG — Retrieval-Augmented Generation](https://weaviate.io/blog/agentic-rag)

---

### Prerequisites

Before running any notebook, make sure the project dependencies are installed and
your API keys are configured:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file at the project folder with your API keys:

```env
OPENAI_API_KEY=your_openai_key_here
CHROMA_OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

**Dependencies:** `openai`, `chromadb`, `tavily-python`, `python-dotenv`, `pydantic`, `pypdf`

---

**Back to:** [Main Index](../README.md)
