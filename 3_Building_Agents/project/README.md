# UdaPlay — AI Research Agent for the Video Game Industry

UdaPlay is an AI Research Agent that answers questions about video games by combining
an internal vector database (ChromaDB) with live web search (Tavily). The agent follows
an Agentic RAG workflow: it always checks the internal database first, evaluates the
quality of the results, and falls back to web search only when needed.

## Getting Started

Follow the steps below to set up your environment and run the project notebooks.

### Dependencies

```
openai
chromadb
tavily-python
pydantic
python-dotenv
```

### Installation

1. **Clone the repository** and navigate to the project folder:

```bash
cd 3_Building_Agents/project
```

2. **Activate the virtual environment** (or create one if needed):

```bash
source ../.venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** at the workspace root (or in the `project/` folder):

```env
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

> **Udacity Workspace:** environment variables are pre-loaded. The notebooks detect
> this automatically and route API calls through the Vocareum proxy
> (`https://openai.vocareum.com/v1`).

5. **Run the notebooks in order:**
   - `Udaplay_01_starter_project.ipynb` — builds the vector database
   - `Udaplay_02_starter_project.ipynb` — builds and runs the agent

---

## Project Instructions

This project is split into two sequential parts. **Complete Part 01 before Part 02**,
as Part 02 depends on the ChromaDB collection created in Part 01.

### Part 01 — Offline RAG: Building the Vector Database

Build a ChromaDB persistent vector store from a set of JSON game records.

**Deliverables:**
1. Instantiate a `chromadb.PersistentClient` (persists to disk across notebooks).
2. Create an `OpenAIEmbeddingFunction` using `text-embedding-3-small`.
3. Create (or recreate) a ChromaDB collection named `udaplay`.
4. Load each `.json` file from the `games/` directory and add it to the collection:
   - Format the document text as: `"[{Platform}] {Name} ({YearOfRelease}) - {Description}"`
   - Use the file name (without extension) as the document ID.
   - Include all original JSON fields as metadata.
5. Confirm the total document count after indexing.

**Expected output:** a persistent `chromadb/` directory with the `udaplay` collection
containing all game documents.

---

### Part 02 — The UdaPlay Agent

Build the UdaPlay AI Research Agent on top of the vector database from Part 01.

**Step 1 — Define three tools:**

| Tool | Description |
|---|---|
| `retrieve_game` | Query the `udaplay` ChromaDB collection (top-5 semantic results) |
| `evaluate_retrieval` | LLM-as-judge: assess if retrieved docs answer the user's question |
| `game_web_search` | Tavily web search — fallback when internal database is insufficient |

**Step 2 — Create the UdaPlay agent:**
- Model: `gpt-4o-mini`
- System instructions that enforce the fixed workflow:
  1. Always call `retrieve_game` first.
  2. Always call `evaluate_retrieval` to assess quality.
  3. Call `game_web_search` only if `evaluate_retrieval` returns `useful=false`.
- Attach all three tools to the agent.

**Step 3 — Run the agent** on at least three queries that exercise different code paths:
- A query answered by the internal database.
- A query that requires web search.

**Step 4 (Optional) — Long-term memory:**
- Set up a `LongTermMemory` store backed by ChromaDB.
- After any run that used `game_web_search`, persist the answer as a `MemoryFragment`.
- Demonstrate retrieval from long-term memory using a related query.

**Expected output:** structured agent responses that declare their source
(*Internal Database*, *Web Search*, or *Internal Database + Web Search*).

---

## Testing

Run each notebook cell in order. The key checkpoints are:

```
# Part 01 — expected after indexing
Collection 'udaplay' created. Documents currently indexed: 15

# Part 02 — expected after agent setup
UdaPlay agent created successfully.
Model: gpt-4o-mini | Tools: ['retrieve_game', 'evaluate_retrieval', 'game_web_search']
```

### Verifying the Agentic RAG Loop

Each agent response should display:
- **QUERY** — the user's question
- **TOOLS** — the sequence of tools called (e.g., `retrieve_game → evaluate_retrieval`)
- **SOURCE** — where the answer came from
- **ANSWER** — the final response with source attribution

Confirm that `game_web_search` is called only when `evaluate_retrieval` returns
`useful=false`, and that the final answer always states its source.

---

## Built With

* [OpenAI API](https://platform.openai.com/docs/) — `gpt-4o-mini` for the agent and
  `text-embedding-3-small` for embeddings
* [ChromaDB](https://docs.trychroma.com/) — persistent vector store for the game database
* [Tavily](https://docs.tavily.com/) — web search API for external knowledge retrieval
* [Pydantic](https://docs.pydantic.dev/) — structured output schema (`EvaluationReport`)
* [python-dotenv](https://pypi.org/project/python-dotenv/) — API key management

## License

[License](../LICENSE.md)
