# Udacity Project — UdaPlay: AI Research Agent for Video Games

## Project: UdaPlay — AI Research Agent for the Video Game Industry

### Project Introduction

Building agents means going beyond simple prompts — it means equipping LLMs with
tools, memory, and the ability to reason about *when* and *how* to act. This project
applies the full agent-building toolkit to solve a real-world information retrieval
challenge: providing accurate, grounded answers about the video game industry.

In this project, I build **UdaPlay**, an AI Research Agent that combines an internal
vector database with web search to answer questions about video games. The system
demonstrates the complete agentic loop: semantic retrieval, quality evaluation, and
dynamic fallback to external sources — all orchestrated by a stateful agent built on
the course's `lib` framework.

---

### Project Summary

The solution is delivered in two parts:

#### Part 01: Offline RAG — Building the Vector Database

A ChromaDB persistent collection (`udaplay`) is built from a set of JSON game records.
Each document is embedded using `text-embedding-3-small` and indexed with full metadata:

```json
{
  "Name": "Gran Turismo",
  "Platform": "PlayStation 1",
  "Genre": "Racing",
  "Publisher": "Sony Computer Entertainment",
  "Description": "A realistic racing simulator featuring a wide array of cars and tracks.",
  "YearOfRelease": 1997
}
```

The notebook handles idempotent collection creation (delete-and-recreate on re-run) and
confirms the total document count after indexing.

#### Part 02: AI Research Agent — UdaPlay

A `gpt-4o-mini`-powered agent (`UdaPlay`) is built on top of the vector database.
The agent follows a strict Agentic RAG workflow using three tools:

| Tool | Purpose |
|---|---|
| `retrieve_game` | Semantic search against the ChromaDB `udaplay` collection (top-5 results) |
| `evaluate_retrieval` | LLM-as-judge (`gpt-4o-mini`, `temperature=0`) assesses if retrieved docs answer the question |
| `game_web_search` | Tavily web search — only triggered when `evaluate_retrieval` returns `useful=false` |

The agent always follows this workflow:

1. **Retrieve** — `retrieve_game` searches the internal database.
2. **Evaluate** — `evaluate_retrieval` judges whether the results suffice.
3. **Web fallback** — `game_web_search` fires only if the internal database is insufficient.
4. **Answer** — a structured response stating the source (Internal Database / Web Search).

An optional extension implements **long-term memory** via `LongTermMemory` + ChromaDB,
persisting web-search findings across sessions.

---

### Architecture Overview

```
User Question
      │
      ▼
UdaPlay Agent (gpt-4o-mini + StateMachine)
      │
      ▼
retrieve_game  ──── semantic search ──▶  ChromaDB 'udaplay' collection (15 docs)
      │
      ▼
evaluate_retrieval  ──── LLM-as-judge ──▶  { useful: bool, description: str }
      │
      ├─▶ useful=true  ──▶  Synthesize answer from Internal Database
      │
      └─▶ useful=false
              │
              ▼
        game_web_search  ──── Tavily API ──▶  web results + direct answer
              │
              ▼
        Synthesize answer from Web Search
      │
      ▼
Structured Response (source declared: Internal DB / Web Search / Both)

(Optional)
      │
      ▼
LongTermMemory  ──── persist web findings ──▶  ChromaDB (in-memory)
```

---

## Project Evaluation Key Points

### Part 01 — Vector Database

**ChromaDB Setup**
- `PersistentClient` created at `chromadb/` path for cross-notebook reuse.
- Collection `udaplay` created with `OpenAIEmbeddingFunction` (`text-embedding-3-small`).
- Idempotent: delete-and-recreate pattern ensures clean re-runs.
- All JSON game files in `games/` are indexed with content string:
  `"[{Platform}] {Name} ({YearOfRelease}) - {Description}"`.
- Document IDs match the file name (without extension).

### Part 02 — Agent Implementation

**Tool Definitions**
- `retrieve_game`: queries `collection.query()` with `n_results=5`, returns formatted
  list of dicts with `Name`, `Platform`, `YearOfRelease`, `Description`, `Genre`,
  `Publisher`, and `similarity_score`.
- `evaluate_retrieval`: calls `judge_llm.invoke()` with `response_format=EvaluationReport`
  (Pydantic model); returns `{"useful": bool, "description": str}`.
- `game_web_search`: calls Tavily with `search_depth="advanced"`, `include_answer=True`,
  `max_results=5`; returns formatted dict with `answer` and up to 3 `sources`.

**Agent Behavior**
- Agent instructions enforce the fixed tool-call order (retrieve → evaluate → web search).
- `temperature=0.2` on the agent; `temperature=0.0` on the judge LLM.
- Source attribution is always declared in the final answer.

**Structured Output**
- `EvaluationReport` Pydantic model with `useful: bool` and `description: str`.
- Final answers declare source: *"Internal Database"*, *"Web Search (Tavily)"*, or
  *"Internal Database + Web Search (Tavily)"*.

---

### Directory Structure

```
3_Building_Agents/
├── README.md                           ← This file
├── docs/                               ← Study guides (Portuguese)
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
├── exercises/                          ← Course exercises (Jupyter notebooks)
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
│   ├── 07-sales.db
│   ├── 08-agentic-rag-demo.ipynb
│   ├── 08-agentic-rag-exercise.ipynb
│   ├── 09-long-term-memory-demo.ipynb
│   ├── 10-agentic-evaluation-demo.ipynb
│   ├── pdf/
│   │   ├── TheGamingIndustry2024.pdf
│   │   └── GlobalEVOutlook2025.pdf
│   └── lib/                            ← Shared Python library
│       ├── agents.py                   ← Agent, StructuredAgent
│       ├── state_machine.py            ← StateMachine, Step, EntryPoint, Termination
│       ├── memory.py                   ← ShortTermMemory, LongTermMemory
│       ├── llm.py                      ← LLM wrapper
│       ├── messages.py                 ← Message types
│       ├── tooling.py                  ← @tool decorator
│       ├── parsers.py                  ← JsonOutputParser, PydanticOutputParser
│       ├── vector_db.py                ← VectorStoreManager
│       ├── rag.py                      ← RAG pipeline utilities
│       ├── loaders.py                  ← Document loaders
│       ├── documents.py                ← Document data class
│       └── evaluation.py              ← AgentEvaluator, TestCase
└── project/
    ├── README.md                       ← Project instructions and deliverables
    ├── Udaplay_01_starter_project.ipynb ← Part 01: ChromaDB setup
    ├── Udaplay_02_starter_project.ipynb ← Part 02: UdaPlay agent
    └── lib/                            ← Same library as exercises/lib
```

---

## Solution

> **Instructor Note:** This section explains the reference solution for the UdaPlay
> project. Read it after you have attempted the implementation on your own.
> Understanding *why* each design decision was made is as important as making the
> code run.

### Workflow

1. **Vector Store Construction (Part 01):**
   Each JSON game file is read, its content formatted as a single string, and added
   to ChromaDB with the file name as document ID and all original fields as metadata.
   The `PersistentClient` ensures the collection survives notebook restarts, allowing
   Part 02 to reuse it without rebuilding.

2. **Agentic RAG Loop (Part 02):**
   The agent always starts with `retrieve_game` — even for questions likely to require
   web search. This ensures the internal database is always consulted first and prevents
   unnecessary API calls. The `evaluate_retrieval` step acts as a semantic gate: the
   judge LLM reads both the question and retrieved documents and decides if they are
   sufficient. Only a `useful=false` verdict unlocks `game_web_search`.

3. **LLM-as-Judge Evaluation:**
   `evaluate_retrieval` uses a separate `LLM` instance (`temperature=0`) to assess
   quality. This isolation keeps the evaluation deterministic and prevents the agent's
   conversational context from biasing the verdict. The `EvaluationReport` Pydantic
   model enforces a structured, typed response.

4. **Web Search Fallback:**
   Tavily's `search_depth="advanced"` with `include_answer=True` provides a direct
   answer alongside raw sources. The agent truncates each source to 400 characters
   before returning, keeping the context window manageable.

5. **Optional Long-Term Memory:**
   Web-search findings are persisted as `MemoryFragment` objects in a `LongTermMemory`
   store backed by an in-memory ChromaDB instance. The `namespace="game_facts"` and
   `owner="udaplay"` scoping allows future retrieval without polluting unrelated memory.

---

### Key Design Decisions

#### 1. Fixed Tool-Call Order via System Prompt

The agent's `UDAPLAY_INSTRUCTIONS` enforce an explicit numbered workflow:
1. `retrieve_game` → 2. `evaluate_retrieval` → 3. (conditional) `game_web_search`.

This eliminates the need for complex routing logic — the LLM's instruction-following
capability enforces the pipeline. The instructions also prohibit skipping steps,
preventing the agent from going directly to web search even when it "thinks" the
internal database won't help.

**Why it matters:** Without this constraint, `gpt-4o-mini` may shortcut to web
search for questions involving recent events, bypassing potentially valid local data.

#### 2. Idempotent Collection Setup

The `delete_collection` + `create_collection` pattern (with `try/except` for the
first run) ensures the notebook can be re-run from scratch without leaving stale data.
This is critical in educational environments where notebooks may be partially executed
or reset.

#### 3. Judge LLM Isolation

A separate `LLM(temperature=0)` instance handles evaluation rather than reusing the
agent's main LLM. This means:
- The judge always returns a structured `EvaluationReport` (not conversational text).
- The agent's message history does not influence the evaluation verdict.
- `temperature=0` makes the accept/reject decision as deterministic as possible.

#### 4. Source Attribution in Every Answer

The agent instructions require declaring whether each answer came from the internal
database, web search, or both. This makes the Agentic RAG loop transparent to the
user and demonstrates grounding — a key requirement in production AI systems.

#### 5. Similarity Score in Retrieval Results

`retrieve_game` converts ChromaDB's distance metric to a similarity score
(`1 - distance`) and includes it in the returned JSON. This allows the evaluator
LLM to factor in retrieval confidence and gives the agent additional signal for
its `evaluate_retrieval` step.

---

### Key Technologies

| Technology | Purpose |
|-----------|---------|
| OpenAI `gpt-4o-mini` | Chat completions for the UdaPlay agent and evaluation judge |
| OpenAI `text-embedding-3-small` | Embedding generation for ChromaDB indexing and retrieval |
| ChromaDB | Persistent vector store for the `udaplay` game collection |
| Tavily | Web search API for external knowledge retrieval |
| Pydantic | Structured output schema (`EvaluationReport`) |
| Vocareum Proxy | API gateway (`base_url="https://openai.vocareum.com/v1"`) for Udacity workspace |
| `python-dotenv` | API key management via `.env` files |
| `lib` (course library) | `Agent`, `StateMachine`, `LongTermMemory`, `@tool`, `LLM`, message types |

---

### Submission

| Part | Artifact |
|------|----------|
| Part 01 | [Udaplay_01_starter_project.ipynb](./project/Udaplay_01_starter_project.ipynb) — ChromaDB setup and document indexing |
| Part 02 | [Udaplay_02_starter_project.ipynb](./project/Udaplay_02_starter_project.ipynb) — UdaPlay agent with tools and Agentic RAG |

---

### Execution Evidence

The agent was executed against three representative queries demonstrating all
code paths in the Agentic RAG workflow:

| Query | Tools Called | Source |
|---|---|---|
| "When was Pokémon Gold and Silver released?" | `retrieve_game` → `evaluate_retrieval` | Internal Database |
| "Which one was the first 3D platformer Mario game?" | `retrieve_game` → `evaluate_retrieval` × 2 | Internal Database |
| "Was Mortal Kombat X released for PlayStation 5?" | `retrieve_game` → `evaluate_retrieval` × 3 → `game_web_search` | Web Search |

The third query demonstrates the full fallback path: after three retrieve-evaluate
cycles returned `useful=false`, the agent correctly escalated to Tavily web search
and returned a grounded answer with source citations.

An optional long-term memory demo stores the Zelda web-search result and confirms
retrieval by querying `namespace="game_facts"` with the query *"Zelda developer"*.

---

### Exercises (Learning Path)

The notebooks below build the skills applied in the project:

| # | Notebook | Topic |
|---|----------|-------|
| 01 | [Tool Calling](./exercises/01-tool-calling-demo.ipynb) | Function calling and the `@tool` decorator |
| 02 | [Structured Outputs](./exercises/02-structured-outputs-demo.ipynb) | Pydantic models and output parsers |
| 03 | [State Machine](./exercises/03-state-machine-demo.ipynb) | Agent state management |
| 04 | [Short-Term Memory](./exercises/04-short-term-memory-demo.ipynb) | Session memory strategies |
| 05 | [External APIs](./exercises/05-external-apis-demo.ipynb) | Resilient API clients and MCP |
| 06 | [Web Search](./exercises/06-web-search-exercise.ipynb) | Web search agents with Tavily |
| 07 | [Databases](./exercises/07-interacting-databases-demo.ipynb) | text2SQL and vector search |
| 08 | [Agentic RAG](./exercises/08-agentic-rag-demo.ipynb) | Retrieve-Reflect-Retry loop |
| 09 | [Long-Term Memory](./exercises/09-long-term-memory-demo.ipynb) | Persistent memory with ChromaDB |
| 10 | [Evaluation](./exercises/10-agentic-evaluation-demo.ipynb) | LLM-as-judge and evaluation strategies |

---

### References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Tavily Search API](https://docs.tavily.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [LLM-as-Judge Evaluation](https://arxiv.org/abs/2306.05685)

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

Create a `.env` file at the workspace root (or the `project/` folder) with:

```env
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

**Dependencies:** `openai`, `chromadb`, `tavily-python`, `pydantic`, `python-dotenv`
