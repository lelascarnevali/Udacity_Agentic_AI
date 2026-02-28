# Udacity Project — AI-Powered Agentic Workflow for Project Management

## Project: Agentic Workflow for Technical Project Management (Pilot: Email Router)

### Project Introduction

Agentic workflows represent the next evolution in AI-powered automation — systems
where AI agents don't just execute predefined tasks, but dynamically *manage* them.
This project applies agentic workflow patterns to solve a real-world challenge:
transforming high-level product ideas into structured, actionable development plans.

In this project, I build an **AI-Powered Agentic Workflow for Project Management**
— a Python-based system that orchestrates multiple specialized agents to assist
Technical Project Managers (TPMs) at **InnovateNext Solutions**, a rapidly scaling
startup. The system converts product specifications into well-defined user stories,
product features, and detailed engineering tasks. The pilot uses their "Email Router"
product specification as input.

---

### Project Summary

The solution is delivered in two phases:

#### Phase 1: The Agentic Toolkit

A reusable Python package (`workflow_agents`) containing seven agent classes, each
demonstrating a distinct agentic pattern:

| Agent Class | Pattern | Purpose |
|---|---|---|
| `DirectPromptAgent` | Direct Prompting | Relays user input directly to an LLM without additional context |
| `AugmentedPromptAgent` | Persona Augmentation | Responds according to a predefined persona |
| `KnowledgeAugmentedPromptAgent` | Knowledge Injection | Incorporates specific knowledge alongside a persona |
| `RAGKnowledgePromptAgent` | Retrieval-Augmented Generation | Dynamic knowledge sourcing via embeddings (provided) |
| `EvaluationAgent` | Evaluator-Optimizer | Iteratively evaluates and refines worker agent outputs |
| `RoutingAgent` | Semantic Routing | Routes prompts to the best-matching agent via cosine similarity |
| `ActionPlanningAgent` | Action Planning | Extracts actionable steps from a user prompt using LLM reasoning |

Each agent is individually tested with a standalone script proving its capabilities.

#### Phase 2: The Project Management Workflow

A primary script (`agentic_workflow.py`) that orchestrates Phase 1 agents to perform
multi-step technical project management:

1. **Action Planning** — An `ActionPlanningAgent` decomposes the high-level goal
   into logical sub-tasks (define stories → define features → define tasks).

2. **Semantic Routing** — A `RoutingAgent` assigns each sub-task to the appropriate
   specialized agent team based on embedding similarity.

3. **Product Manager Team** — A `KnowledgeAugmentedPromptAgent` generates user
   stories from the product spec, validated by an `EvaluationAgent` ensuring the
   format: *"As a [user], I want [action] so that [benefit]."*

4. **Program Manager Team** — A `KnowledgeAugmentedPromptAgent` defines product
   features, validated by an `EvaluationAgent` ensuring Feature Name, Description,
   Key Functionality, and User Benefit structure.

5. **Development Engineer Team** — A `KnowledgeAugmentedPromptAgent` creates
   detailed engineering tasks, validated by an `EvaluationAgent` ensuring Task ID,
   Title, Related Story, Description, Acceptance Criteria, Effort, and Dependencies.

6. **Structured Output** — The workflow produces a comprehensive project plan for
   the Email Router, demonstrating the system's capability.

---

### Architecture Overview

```
workflow_prompt (TPM request)
      │
      ▼
ActionPlanningAgent  ──── extract steps from knowledge ──▶  workflow_steps[]
      │
      ▼
RoutingAgent  ──── cosine similarity routing ──▶  best agent team
      │
      ├─▶ Product Manager Team
      │     KnowledgeAugmentedPromptAgent → EvaluationAgent → user stories
      │
      ├─▶ Program Manager Team
      │     KnowledgeAugmentedPromptAgent → EvaluationAgent → product features
      │
      └─▶ Development Engineer Team
            KnowledgeAugmentedPromptAgent → EvaluationAgent → engineering tasks
      │
      ▼
Final Structured Output (project plan)
```

---

## Project Evaluation Key Points

### Phase 1 — Agent Implementation

**Agent Classes (base_agents.py)**
- All six student-implemented agent classes are defined with correct `__init__`
  and primary public methods.
- `DirectPromptAgent`: passes user prompt directly as a user message without system
  prompt; returns text content only.
- `AugmentedPromptAgent`: uses system prompt for persona + instruction to forget
  previous context; returns text content only.
- `KnowledgeAugmentedPromptAgent`: system prompt sets persona, injects knowledge,
  instructs LLM to use only provided knowledge; returns text content only.
- `EvaluationAgent`: iterative loop up to `max_interactions`; evaluates worker output
  against criteria; generates correction instructions; returns dict with
  `final_response`, `evaluation`, and iteration count. Uses `temperature=0`.
- `RoutingAgent`: computes embeddings via `text-embedding-3-large`; calculates
  cosine similarity; selects best agent; calls its function.
- `ActionPlanningAgent`: system prompt defines action planning role; extracts steps
  from prompt; returns clean list of steps.

**Agent Testing**
- Separate test script for each of the six implemented agents.
- Each script imports, instantiates, calls primary method, and prints results.
- Evidence of successful execution (screenshots or terminal output).

### Phase 2 — Workflow Implementation

**Setup and Agent Instantiation**
- Correct imports from `workflow_agents.base_agents`.
- OpenAI API key loaded from environment variables.
- `Product-Spec-Email-Router.txt` loaded into `product_spec`.
- All knowledge/evaluation agents correctly instantiated per role.
- `RoutingAgent` configured with routes for Product Manager, Program Manager,
  and Development Engineer.

**Workflow Logic and Execution**
- Support functions accept query → call knowledge agent → evaluate → return
  final validated response.
- Main workflow uses `ActionPlanningAgent` to get steps, iterates through them
  via `RoutingAgent`, collects results, and prints final output.

**Structured Output**
- User stories follow: *"As a [type of user], I want [action] so that [benefit]."*
- Features follow: Feature Name, Description, Key Functionality, User Benefit.
- Tasks follow: Task ID, Task Title, Related User Story, Description, Acceptance
  Criteria, Estimated Effort, Dependencies.

---

### Directory Structure

```
2_Agentic_Workflows/
├── README.md                           ← This file
├── docs/                               ← Study guides (Portuguese)
│   ├── 01-introduction-to-agentic-workflows.md
│   ├── 02-the-modern-ai-agent.md
│   ├── 03-agentic-workflow-modeling.md
│   ├── 04-agentic-workflow-patterns-prompt-chaining.md
│   ├── 05-agentic-workflow-patterns-routing.md
│   ├── 06-agentic-workflow-patterns-parallelization.md
│   ├── 07-agentic-workflow-patterns-evaluator-optimizer.md
│   └── README.md
├── exercises/                          ← Course exercises (Python scripts)
│   ├── 1-starter.py
│   ├── 4-prompt-chaining.py
│   ├── 5-agentic-routing.py
│   ├── 6-agentic-parallelization.py
│   ├── 7-agentic-evaluator-optimizer.py
│   └── *-demo.py                       ← Demo scripts
└── project/
    ├── evidence/                        ← Execution outputs (terminal captures)
    │   ├── 01-direct_prompt_agent_output.txt
    │   ├── 02-augmented_prompt_agent_output.txt
    │   ├── 03-knowledge_augmented_prompt_agent_output.txt
    │   ├── 04-rag_knowledge_prompt_agent_output.txt
    │   ├── 05-evaluation_agent_output.txt
    │   ├── 06-routing_agent_output.txt
    │   ├── 07-action_planning_agent_output.txt
    │   └── 08-agentic_workflow_output.txt
    ├── phase_1/
    │   ├── workflow_agents/
    │   │   ├── __init__.py
    │   │   └── base_agents.py          ← Agent library implementation
    │   ├── direct_prompt_agent.py       ← Test scripts
    │   ├── augmented_prompt_agent.py
    │   ├── knowledge_augmented_prompt_agent.py
    │   ├── rag_knowledge_prompt_agent.py
    │   ├── evaluation_agent.py
    │   ├── routing_agent.py
    │   ├── action_planning_agent.py
    │   └── README.md
    └── phase_2/
        ├── workflow_agents/
        │   ├── __init__.py
        │   └── base_agents.py          ← Copied from Phase 1
        ├── Product-Spec-Email-Router.txt
        ├── agentic_workflow.py          ← Workflow orchestration
        └── README.md
```

---

## Solution

> **Instructor Note:** This section explains the reference solution for the
> AI-Powered Agentic Workflow project. Read it after you have attempted the
> implementation on your own. Understanding *why* each design decision was made
> is as important as making the code run.

### Reference Files

| Phase | File | Description |
|-------|------|-------------|
| Phase 1 | [base_agents.py](./project/phase_1/workflow_agents/base_agents.py) | Agent library — 7 classes (6 student-implemented + 1 provided) |
| Phase 1 | [direct_prompt_agent.py](./project/phase_1/direct_prompt_agent.py) … [action_planning_agent.py](./project/phase_1/action_planning_agent.py) | Individual test scripts (7 total) |
| Phase 2 | [agentic_workflow.py](./project/phase_2/agentic_workflow.py) | Full orchestration script |
| Phase 2 | [Product-Spec-Email-Router.txt](./project/phase_2/Product-Spec-Email-Router.txt) | Input product specification |

---

### Workflow

1. **Listing Generation → Agent Library (Phase 1):**
   Each agent class encapsulates a distinct agentic pattern. The `DirectPromptAgent`
   sends raw user input without system context. The `AugmentedPromptAgent` injects a
   persona via system prompt with an explicit "Forget all previous context" instruction.
   The `KnowledgeAugmentedPromptAgent` adds domain knowledge alongside the persona,
   instructing the LLM to answer *only* from provided knowledge.

2. **Evaluation Loop (Phase 1):**
   The `EvaluationAgent` orchestrates an iterative generate → evaluate → instruct →
   refine cycle. A worker agent produces a response, then a separate evaluator LLM call
   (at `temperature=0`) judges it against criteria. If rejected, the evaluator generates
   correction instructions that are fed back to the worker. This continues up to
   `max_interactions` rounds until accepted.

3. **Semantic Routing (Phase 1):**
   The `RoutingAgent` uses `text-embedding-3-large` to embed both the user input and
   each candidate agent's description. Cosine similarity determines the best-matching
   agent, whose function is then called. This eliminates brittle keyword matching in
   favor of semantic understanding.

4. **Action Planning (Phase 1):**
   The `ActionPlanningAgent` receives domain knowledge about the product development
   lifecycle and extracts an ordered list of steps from the user's high-level prompt.

5. **End-to-End Orchestration (Phase 2):**
   The `agentic_workflow.py` script loads the Email Router product spec, then:
   - `ActionPlanningAgent` decomposes the goal into ~9 sub-tasks
   - Each sub-task is routed via `RoutingAgent` to one of three specialized teams
   - Each team's support function chains: `KnowledgeAugmentedPromptAgent` → `EvaluationAgent`
   - Validated results are collected and printed as the final project plan

---

### Key Design Decisions

#### 1. "Forget All Previous Context" in System Prompts

Both `AugmentedPromptAgent` and `KnowledgeAugmentedPromptAgent` include the
instruction *"Forget all previous context"* in their system prompts. This ensures
each call behaves as a stateless interaction, preventing cross-contamination between
sequential agent invocations within the same workflow.

**Why it matters:** In the Phase 2 workflow, the same `KnowledgeAugmentedPromptAgent`
instance is called repeatedly across different sub-tasks. Without this guard, the LLM
could carry forward context from a previous step, producing user stories when asked
for engineering tasks.

#### 2. Knowledge Injection Over RAG for Role Agents

The Product Manager, Program Manager, and Development Engineer agents use
`KnowledgeAugmentedPromptAgent` (direct knowledge injection) rather than
`RAGKnowledgePromptAgent` (embedding-based retrieval). This is intentional: the
knowledge for each role is compact enough to fit entirely in the system prompt, making
chunk-and-embed overhead unnecessary. RAG is reserved for scenarios where the corpus
is too large for a single prompt window.

**Lesson:** RAG adds latency and complexity. Use direct injection when the knowledge
fits in context; reserve RAG for truly large corpora.

#### 3. Evaluator Criteria as Structured Format Specifications

Each `EvaluationAgent` receives criteria that specify an *exact output structure*
rather than a subjective quality judgment:
- Product Manager: `"As a [type of user], I want [action] so that [benefit]"`
- Program Manager: `"Feature Name, Description, Key Functionality, User Benefit"`
- Development Engineer: `"Task ID, Task Title, Related User Story, Description, Acceptance Criteria, Estimated Effort, Dependencies"`

This converts the evaluator from a vague quality gate into a **structural validator**,
making the accept/reject decision deterministic and auditable.

#### 4. Route Descriptions as Disambiguation Contracts

The `RoutingAgent` agent descriptions include negative constraints:
- Product Manager: *"Does not define features or tasks. Does not group stories."*
- Program Manager: *"Does not define user stories or engineering tasks."*
- Development Engineer: *"Does not define user stories or features."*

This pushes the embedding vectors apart, reducing overlap and improving routing
accuracy for ambiguous prompts like "defining features based on user stories."

#### 5. Support Functions as Composition Pattern

Each role's support function (`product_manager_support_function`, etc.) follows the
same pattern: `knowledge_agent.respond(query)` → `evaluation_agent.evaluate(response)`.
This composition is explicit rather than hidden inside a framework, making the data
flow transparent and debuggable.

---

### Key Technologies

| Technology | Purpose |
|-----------|---------|
| OpenAI `gpt-3.5-turbo` | Chat completions for all agent responses and evaluations |
| OpenAI `text-embedding-3-large` | Embedding generation for semantic routing |
| Vocareum Proxy | API gateway (`base_url="https://openai.vocareum.com/v1"`) |
| `python-dotenv` | API key management via `.env` files |
| `numpy` | Cosine similarity calculations |
| `pandas` | Data handling in RAG agent |

---

### Submission

| Phase | Artifact |
|-------|----------|
| Phase 1 | [base_agents.py](./project/phase_1/workflow_agents/base_agents.py) — Agent library |
| Phase 1 | [Test scripts](./project/phase_1/) — 7 individual agent test scripts |
| Phase 2 | [agentic_workflow.py](./project/phase_2/agentic_workflow.py) — Workflow orchestration |
| Evidence | [project/evidence/](./project/evidence/) — Terminal output captures (8 files) |

---

### Execution Evidence

All agents were executed against the Vocareum OpenAI proxy
(`base_url="https://openai.vocareum.com/v1"`) and their terminal outputs
captured in [`project/evidence/`](./project/evidence/).

#### Phase 1 — Individual Agent Tests

| # | Agent | Evidence File | Key Result |
|---|-------|---------------|------------|
| 01 | `DirectPromptAgent` | [01-direct_prompt_agent_output.txt](./project/evidence/01-direct_prompt_agent_output.txt) | Correctly answered "The capital of France is Paris." using only LLM knowledge |
| 02 | `AugmentedPromptAgent` | [02-augmented_prompt_agent_output.txt](./project/evidence/02-augmented_prompt_agent_output.txt) | Responded with college professor persona |
| 03 | `KnowledgeAugmentedPromptAgent` | [03-knowledge_augmented_prompt_agent_output.txt](./project/evidence/03-knowledge_augmented_prompt_agent_output.txt) | Used injected knowledge ("London, not Paris") — proves knowledge overrides LLM training data |
| 04 | `RAGKnowledgePromptAgent` | [04-rag_knowledge_prompt_agent_output.txt](./project/evidence/04-rag_knowledge_prompt_agent_output.txt) | Provided agent — process killed due to large embedding computation |
| 05 | `EvaluationAgent` | [05-evaluation_agent_output.txt](./project/evidence/05-evaluation_agent_output.txt) | 2 iterations: refined response from sentence → single city name ("London.") |
| 06 | `RoutingAgent` | [06-routing_agent_output.txt](./project/evidence/06-routing_agent_output.txt) | All 3 prompts routed correctly: Texas→texas agent (0.386), Rome Italy→europe agent (0.288), Math→math agent (0.130) |
| 07 | `ActionPlanningAgent` | [07-action_planning_agent_output.txt](./project/evidence/07-action_planning_agent_output.txt) | Extracted 8 scrambled eggs recipe steps from knowledge |

#### Phase 2 — Full Agentic Workflow

| Evidence File | Steps Processed | Lines |
|---|---|---|
| [08-agentic_workflow_output.txt](./project/evidence/08-agentic_workflow_output.txt) | 9 | 1696 |

The workflow processed the prompt *"What would the development tasks for this
product be?"* through the full pipeline:

1. `ActionPlanningAgent` decomposed the goal into 9 sub-tasks.
2. `RoutingAgent` assigned each sub-task to the best team via cosine similarity.
3. Each team's `KnowledgeAugmentedPromptAgent` + `EvaluationAgent` generated and
   validated structured outputs (user stories, features, and engineering tasks).
4. Final output: a complete project plan for the Email Router product.

---

### Exercises (Learning Path)

The scripts below build the skills applied in the project:

| # | Script | Topic |
|---|--------|-------|
| 01 | [Starter](./exercises/1-starter.py) | Introduction to agentic workflows |
| 04 | [Prompt Chaining](./exercises/4-prompt-chaining.py) | Prompt chaining pattern |
| 05 | [Agentic Routing](./exercises/5-agentic-routing.py) | Routing pattern with embeddings |
| 06 | [Agentic Parallelization](./exercises/6-agentic-parallelization.py) | Parallelization pattern |
| 07 | [Evaluator-Optimizer](./exercises/7-agentic-evaluator-optimizer.py) | Evaluator-optimizer pattern |

---

### References

- [What Is a Technical Project Manager?](https://www.coursera.org/articles/technical-project-manager)
- [Epic vs Feature vs User Story: Understanding the Hierarchy](https://www.visual-paradigm.com/guide/agile-software-development/epic-vs-feature-vs-user-story/)
- [What are Epics and Features?](https://www.atlassian.com/agile/project-management/epics)
- [Product Backlog](https://www.scrum.org/resources/what-is-a-product-backlog)
- [What is a task in Agile?](https://www.atlassian.com/agile/project-management/tasks)

---

### Prerequisites

Before running any script, make sure the project dependencies are installed and
your API key is configured:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file at the project folder (or `phase_1`/`phase_2`) with your
OpenAI key:

```env
OPENAI_API_KEY=your_key_here
```

**Dependencies:** `openai==1.78.1`, `python-dotenv==1.1.0`, `pandas==2.2.3`
