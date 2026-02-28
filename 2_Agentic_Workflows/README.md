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
