# Udacity Project — Prompting for Effective LLM Reasoning and Planning

## Project: AgentsVille Trip Planner

### Project Introduction

Effective prompt engineering is one of the most critical skills in Agentic AI.
Rather than relying on a single, static query, this project teaches you to craft
multi-stage prompts, feedback loops, and tool-calling agents that can reason
step-by-step and revise their own outputs.

In this project, I build the **AgentsVille Trip Planner** — a Jupyter Notebook
application that interacts with an LLM to generate, evaluate, and iteratively
refine a day-by-day travel itinerary for a fictional city called *AgentsVille*.

---

### Project Summary

The application is structured as a progressive pipeline:

1. **Define Vacation Details** — Specify trip duration, interests, and constraints.
   Use `Pydantic` to structure and validate this information inside a `VacationInfo`
   model.

2. **Review Weather & Activity Schedules** — Simulate API calls to gather weather
   data and available activities in bulk, then review the data to understand the
   available options.

3. **The ItineraryAgent** — Implement an agent that generates a complete day-by-day
   itinerary based on the vacation details. The system prompt guides the LLM through
   a Chain-of-Thought planning process, with role, task, output format, examples, and
   context all carefully crafted to elicit the best possible plan in one LLM call.

4. **Evaluating the Itinerary** — Evaluate the itinerary against a set of quality
   criteria: matching city and dates, accurate cost calculations, absence of
   hallucinated activities, and weather compatibility. An LLM-powered evaluation
   function compares activity descriptions against weather data.

5. **Defining the Tools** — Four tools assist the revision agent:
   - `calculator_tool` — accurately calculate costs.
   - `get_activities_by_date_tool` — retrieve activities for a specific date.
   - `run_evals_tool` — evaluate the itinerary against all criteria.
   - `final_answer_tool` — return the final structured answer.

6. **The ItineraryRevisionAgent** — A second agent that revises the itinerary using
   the ReAct **THOUGHT → ACTION → OBSERVATION** cycle, incorporating traveler
   feedback (at least 2 activities per day) and iterating until all evaluation
   criteria pass.

7. **Something Just for Fun!** — A narrative summary of the trip, highlighting the
   best activities and experiences.

---

## Project Evaluation Key Points

### General Prompt Design

**`ITINERARY_AGENT_SYSTEM_PROMPT`**
- Clearly instructs the LLM to assume the role of an expert travel planner.
- Encourages detailed daily plans through Chain-of-Thought guidance or examples.
- Specifies JSON output format matching the `TravelPlan` Pydantic model structure.
- Provides necessary context, including the `VacationInfo` object, weather data, and
  activity data.

**`ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT`**
- Clearly defines the LLM role and task (assess compatibility of an activity with
  current weather conditions).
- Specifies exact output format.
- Includes relevant examples illustrating expected evaluations.

---

### Agent Reasoning and Tool Use

**`get_activities_by_date_tool` docstring**
- Provides sufficient description for understanding the tool's purpose and use.
- Defines expected input parameters, their data types, and expected formats.

**`ITINERARY_REVISION_AGENT_SYSTEM_PROMPT`**
- Clearly states the LLM role and itinerary revision task.
- Details the **THINK-ACT-OBSERVE** cycle explicitly.
- Lists all available tools, their purposes, and parameter requirements (added
  dynamically to keep the prompt always up to date).
- Specifies the exact ACTION format for tool invocation:
  ```json
  {"tool_name": "[tool_name]", "arguments": {"arg1": "value1", ...}}
  ```
- Includes an explicit exit instruction: the agent must invoke `final_answer_tool`
  after `run_evals_tool` passes all criteria.

---

### Structured Output Validation

**`VacationInfo` Pydantic model**
- Created properly from the JSON structure representing travelers and vacation
  details.
- Start and end dates are correctly read when fetching weather and activity data.

**`TravelPlan` Pydantic model schema**
- Included in at least one system prompt that must output a `TravelPlan` structure.
- Ideally included in both prompts that produce structured travel output.

---

### General Success Criteria

- `ITINERARY_AGENT_SYSTEM_PROMPT` consistently guides the LLM to produce JSON
  output that validates against the `TravelPlan` Pydantic model and reflects the
  user's preferences.
- `ITINERARY_REVISION_AGENT_SYSTEM_PROMPT` enables the LLM to:
  - Always return a single message containing both a `THOUGHT` and an `ACTION`.
  - Use reasoning within `THOUGHT` to select the right tools at the right time.
  - Generate valid tool calls in the specified JSON format.
  - Invoke `final_answer_tool` only after all evaluation criteria have passed.
- The final itinerary passes all evaluation criteria and incorporates the initial
  traveler feedback.

---

## Solution

Project — [Notebook: project_starter.ipynb](./exercises/project_starter.ipynb)

### Exercises (Learning Path)

The notebooks below build the skills applied in the final project:

| # | Notebook | Topic |
|---|----------|-------|
| 01 | [Introduction to Prompting](./exercises/01-introduction-to-prompting-for-llm-reasoning-and-planning.ipynb) | Foundations of LLM prompting |
| 02 | [Model Selection](./exercises/02-model-selection.ipynb) | Choosing the right model for the task |
| 03 | [Role-Based Prompting](./exercises/03-lesson-1-role-based-prompting.ipynb) | Persona design and role engineering |
| 04 | [Chain-of-Thought & ReAct (Part I)](./exercises/04-lesson-2-chain-of-thought-and-react-prompting-part-i.ipynb) | CoT reasoning patterns |
| 05 | [Chain-of-Thought & ReAct (Part II)](./exercises/05-lesson-2-chain-of-thought-and-react-prompting-part-ii.ipynb) | ReAct and tool-calling loops |
| 06 | [Prompt Instruction Refinement](./exercises/06-lesson-3-prompt-instruction-refinement.ipynb) | Iterative prompt debugging |
| 07 | [Chaining Prompts for Agentic Reasoning](./exercises/07-lesson-4-chaining-prompts-for-agentic-reasoning.ipynb) | Multi-step prompt pipelines |
| 08 | [LLM Feedback Loops](./exercises/08-lesson-5-implementing-llm-feedback-loops.ipynb) | Self-correcting agents |

### Prerequisites

Before running any notebook, make sure the project dependencies are installed and
your API key is configured:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file at the repository root with your OpenAI key:

```env
OPENAI_API_KEY=your_key_here
```

### Key Libraries

| Library | Purpose |
|---------|---------|
| `openai` | LLM API calls |
| `pydantic` | Structured output validation |
| `python-dotenv` | Environment variable management |
| `pandas` | Data manipulation for weather/activity data |
| `numexpr` | Fast numerical evaluation in cost calculations |
| `json-repair` | Tolerant JSON parsing of LLM responses |
