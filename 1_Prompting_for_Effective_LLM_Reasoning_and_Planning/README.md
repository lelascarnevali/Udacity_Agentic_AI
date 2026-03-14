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

> **Instructor Note:** This section explains the reference solution for the AgentsVille Trip Planner project.
> Read it after you have attempted the notebook on your own. Understanding *why* each design decision was made
> is as important as making the code run.

### Reference Notebook

Open and run [project_starter.ipynb](project_starter.ipynb) cell by cell.
Each section maps directly to a rubric criterion described below.

---

### Architecture Overview

The solution implements a **two-agent pipeline** connected by a shared evaluation harness:

```
VacationInfo (Pydantic)
      │
      ▼
ItineraryAgent  ──── Chain-of-Thought prompt ───▶  TravelPlan (draft)
      │
      ▼
Evaluation Harness  ──── eval_* functions ──▶  EvaluationResults
      │
      ▼
ItineraryRevisionAgent  ──── ReAct loop (THOUGHT → ACTION → OBSERVATION) ──▶  TravelPlan (final)
```

This separation of concerns is intentional: the first agent optimises for *quality of reasoning*
(single LLM call, rich context), while the second optimises for *reliability of output*
(iterative tool use, self-evaluation before committing).

---

### Key Design Decisions

#### 1. Chain-of-Thought in `ITINERARY_AGENT_SYSTEM_PROMPT`

The prompt explicitly enumerates five reasoning steps — date alignment, interest matching,
weather constraints, budget calculation, and activity coverage — before asking for the JSON output.
This forces the model to *plan before it writes*, which dramatically reduces schema validation failures
compared to a direct instruction like "produce a travel plan".

**Why it matters for the rubric:** the TravelPlan schema and the ANALYSIS section both appear in
the prompt, so the model has a contract to satisfy *before* generating the FINAL OUTPUT block.

#### 2. Deterministic Output Format in `ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT`

The prompt instructs the model to emit **exactly one word** on the FINAL ANSWER line —
either `IS_COMPATIBLE` or `IS_INCOMPATIBLE`, with no other text, punctuation, or explanation.
This constraint is critical because the downstream Python parser uses substring matching:
if the model outputs both tokens in the same line (e.g. `IS_COMPATIBLE / IS_INCOMPATIBLE`),
the check `"IS_COMPATIBLE" in resp` will always evaluate to `True`, silently masking
incompatible activities.

**Lesson:** when an LLM response drives a conditional branch in production code, the output
format specification must be *unambiguous and mutually exclusive*.

#### 3. Tool Docstrings as Agent Context

The `ItineraryRevisionAgent` system prompt is generated dynamically via
`get_tool_descriptions_string(ALL_TOOLS)`, which reads each tool's `__doc__` string at
instantiation time. This means the docstring is not just for human readers — it is the
primary specification the LLM uses when deciding *how to call the tool*.

The `get_activities_by_date_tool` docstring therefore must declare:
- **parameter names and types** (`date: str`, `city: str`)
- **expected date format** (`YYYY-MM-DD`, e.g. `"2025-06-10"`)
- **return type and structure** (`List[dict]`, each matching the Activity schema)

Omitting this information causes the agent to guess formats, leading to tool-call errors
that waste steps in the ReAct loop.

#### 4. ReAct Loop with Mandatory Exit Gate

The `ITINERARY_REVISION_AGENT_SYSTEM_PROMPT` contains an explicit rule:
> "Call `final_answer_tool` **only** when the most recent `run_evals_tool` call returned
> `success: true` with an empty `failures` list."

This single constraint converts a free-form generation loop into a *verified* loop:
the agent cannot self-certify completion — it must receive external confirmation from the
evaluation harness. This pattern (generate → evaluate → reflect → revise) is the
foundation of self-correcting agentic systems.

---

### Expected Outcomes After Each Stage

| Stage | Artifact | Acceptance criterion |
|-------|----------|----------------------|
| Pydantic validation | `VacationInfo` | All fields present with correct types |
| ItineraryAgent | `travel_plan_1` | JSON validates against `TravelPlan` schema |
| eval_* suite | `EvaluationResults` | Failures listed; `success` may be `False` initially |
| ItineraryRevisionAgent | `travel_plan_2` | `success=True`, `failures=[]` across all 7 evals |

---

### Rubric Alignment

| Rubric criterion | Where implemented |
|------------------|--------------------|
| Role and task definition | `ITINERARY_AGENT_SYSTEM_PROMPT` — role block + numbered reasoning steps |
| Structured output format | Both system prompts specify JSON schema or single-label output |
| Context injection | Weather and activity DataFrames serialised into the ItineraryAgent prompt |
| Tool docstring completeness | `get_activities_by_date_tool` — typed parameters, date format, return type |
| Weather-compatibility evaluation | `ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT` — single-label output rule |
| ReAct loop correctness | `ITINERARY_REVISION_AGENT_SYSTEM_PROMPT` — phased strategy + exit gate |
| Traveler feedback incorporation | `eval_traveler_feedback_is_incorporated` added to `ALL_EVAL_FUNCTIONS` |

---

### Common Pitfalls and Debugging Guide

**The agent produces invalid JSON.**
Check the `ANALYSIS` section in the raw response. If the model reasoned correctly but
formatted incorrectly, strengthen the output format section of the prompt (add an explicit
example with the schema filled in). Also verify that the JSON schema of `TravelPlan` is
included in the prompt context.

**`eval_total_cost_is_accurate` fails.**
The model miscalculated the sum. This is an arithmetic reliability issue — ensure the
`calculator_tool` is available and that the revision agent prompt instructs it to use the
calculator before setting `total_cost`.

**`eval_itinerary_events_match_actual_events` fails with "not matching".**
The model copied an activity but mutated a field (e.g., changed `price` or `start_time`).
Reinforce in the prompt: *"Copy every activity field exactly from the dataset; do not
invent or change any field value."*

**`eval_activities_and_weather_are_compatible` flags a false positive.**
Check whether the activity description explicitly mentions indoor alternatives. If it does,
the prompt rule ("treat it as compatible if it mentions indoor alternatives or backup options")
should handle it. If it still fails, it may be a model hallucination in the evaluator itself —
inspect the `REASONING` section printed to the notebook output.

**The ReAct loop hits `max_steps` without calling `final_answer_tool`.**
Read each THOUGHT/ACTION/OBSERVATION trace to find where the loop stalls. Common causes:
(1) the agent calls `run_evals_tool` with a malformed plan, (2) it ignores an OBSERVATION
and repeats the same action, or (3) the prompt's exit gate condition is unclear.
Increase specificity of the phased strategy section in the revision prompt.


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
