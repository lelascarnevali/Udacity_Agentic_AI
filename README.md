# Udacity Agentic AI Nanodegree

This repository contains the projects and exercises developed as part of the **Agentic AI Nanodegree program** by Udacity. Throughout this program, we go beyond single chatbots to engineer sophisticated, coordinated teams of AI agents.

The curriculum covers advanced prompting techniques, agentic workflows, and the architecture of intelligent systems, enabling the creation of agents that can reason, plan, and use tools to interact with the world.

## Program Overview

The Nanodegree focuses on building agents in Python that can reason, plan, and use tools to interact with databases and external APIs. The program is divided into four main courses:

### 1. Prompting for Effective LLM Reasoning and Planning
Go beyond basic chatbots and learn to engineer sophisticated AI agents. This course covers:
*   **Advanced Prompting:** Master Chain-of-Thought, ReAct, and feedback loops.
*   **Reasoning & Planning:** Build systems that can reason, plan, and solve complex problems.
*   **Hands-on Project:** Transform generic AI into specialized, reliable tools, culminating in building a multi-agent travel planner from scratch.

### 2. Agentic Workflows
Move beyond simple automation and learn to architect intelligent systems using Python. Key concepts include:
*   **Workflow Patterns:** Explore core patterns like Prompt Chaining, Routing, and Parallelization.
*   **Intelligent Teams:** Create teams of AI agents that can reason, plan, and act to solve complex problems.
*   **Hands-on Project:** Build a complete, agentic project management system to translate high-level goals into powerful, adaptive AI solutions.

### 3. Building Agents
Focus on building robust, data-driven AI agents. This course teaches you to:
*   **Tool Integration:** Integrate tools via function calling and generate structured outputs with Pydantic.
*   **State & Memory:** Manage agent state and utilize short-term and long-term memory.
*   **External Interaction:** Create agents that interact with APIs, search the web, query SQL databases, and perform agentic RAG for dynamic retrieval.
*   **Evaluation:** Learn to evaluate agent performance for reliable, real-world applications.

### 4. Multi-Agent Systems
Learn to build coordinated teams of AI agents. This course covers the entire process of creating multi-agent systems:
*   **Architectural Design:** Orchestrate complex workflows from design to implementation in Python.
*   **Data Flow & State:** Manage data flow and state across multiple agents.
*   **Advanced Techniques:** Implement advanced techniques like multi-agent RAG.
*   **Hands-on Project:** Build an automated sales system to solve real-world problems.

---

## Quickstart

Get up and running fast on macOS with `uv` and Jupyter:

```bash
# Clone and enter repository
git clone https://github.com/lelascarnevali/Udacity_Agentic_AI.git
cd Udacity_Agentic_AI

# Create and activate Python 3.13 virtual env
uv venv --python 3.13.0 .venv
source .venv/bin/activate

# Install dependencies and Jupyter
uv pip install -r requirements.txt
uv pip install jupyter

# Launch notebooks
jupyter notebook
# or
jupyter lab
```

Add your API key in a `.env` at the repo root before running notebooks:

```env
OPENAI_API_KEY=your_key_here
```

## Environment Setup

This project uses **[uv](https://github.com/astral-sh/uv)** for fast Python package management.

### Prerequisites

*   **uv installed:** If you don't have it, install it via curl (macOS/Linux) or PowerShell (Windows):
    ```bash
    # macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lelascarnevali/Udacity_Agentic_AI.git
    cd Udacity_Agentic_AI
    ```

2.  **Create a virtual environment (Python 3.13):**
    ```bash
    uv venv --python 3.13.0 .venv
    ```

3.  **Activate the environment:**
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```

4.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    uv pip install jupyter
    ```

### Configuration

**API Key Setup:**
Create a `.env` file in the root directory (based on `.env.example` if available, or just create one) and add your API credentials. This is required for the notebooks to run properly.

```env
OPENAI_API_KEY=your_key_here
```

## Repository Structure

```
.
├── .github/                                   # Copilot configuration and support assets
│   └── skills/                                # Copilot "skills" docs and helper scripts
├── 1_Prompting_for_Effective_LLM_Reasoning_and_Planning/ # Module 1: Prompting foundations
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 2_Agentic_Workflows/                       # Module 2: Designing agentic workflows
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 3_Building_Agents/                         # Module 3: Implementing agents
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 4_Multi-Agent_Systems/                     # Module 4: Multi-agent systems
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── scripts/                                   # Reusable Python utilities for notebooks
└── .venv/                                     # Local Python virtual environment (optional)
```

## Usage

- Activate the environment and launch Jupyter:

```bash
source .venv/bin/activate
uv pip install jupyter
jupyter notebook
```

- Open notebooks under the module `exercises/` folders and run cells.
- Ensure your `.env` contains required keys before running cells that call external APIs.
- Tip: You can also use VS Code to open `.ipynb` files directly for a richer editor experience.

## Development Standards

- Python: follow PEP 8; prefer type hints and concise docstrings; use `black`/`ruff` when applicable.
- Notebooks: write formulas in LaTeX within markdown cells.
    - Inline: `$E=mc^2$`
    - Block: `$$\int_a^b f(x)\,dx$$`
- Commits: use Conventional Commits for clarity (e.g., `feat:`, `chore:`, `docs:`).

---
*Each project in this repository represents a hands-on application of the concepts learned, reinforcing job-ready skills in the field of Agentic AI.*
