# Chaining Prompts for Agentic Reasoning

## Resumo
- **O que:** Padrões para encadear prompts em workflows agentivos.
- **Por que:** Evita halluci­nações e permite validações entre etapas (gate checks).
- **Como:** Decomponha tarefas, defina critérios de sucesso e use validações estruturadas (ex.: Pydantic, ast).

## 1) Why Prompt Chaining Matters

Large Language Models (LLMs) are strong at single-turn generation, but they struggle in multi-stage workflows, especially when tasks require external data (for example: weather, calendar, inventory, policy APIs).

AI agents solve this by combining reasoning with execution:

$$
	ext{Agent} = \text{LLM (reason)} + \text{Tools (act)} + \text{Orchestration (control)}
$$

### Common components of an AI Agent

- **LLM**: the reasoning engine.
- **Tools**: APIs/functions for retrieval and actions.
- **Instructions**: system-level behavior and constraints.
- **Memory**: short-term context + long-term history.
- **Runtime/Orchestration Layer**: controls the loop and tool usage.

To achieve complex goals, agents decompose tasks into smaller steps and evaluate progress at each step.

---

## 2) Prompt Chaining: Core Idea

Prompt chaining programmatically connects outputs and inputs across calls:

$$
	ext{Output}_1 \rightarrow \text{Input}_2,\quad \text{Output}_2 \rightarrow \text{Input}_3
$$

### Example: LinkedIn post workflow

1. **Research** → `RESPONSE_1`
2. **Summarize** using `RESPONSE_1` → `RESPONSE_2`
3. **Draft post** using `RESPONSE_2` → `FINAL_RESPONSE`

This pipeline is more controllable and maintainable than one giant prompt.

---

## 3) Why Chaining Is Essential for Agents

Question: **"What time is my dental appointment tomorrow?"**

### Hard-coded workflow
1. Ask model whether calendar data is needed.
2. If yes, call `get_calendar()`.
3. Ask model to answer from tool output.

### Agentic (ReAct-style) workflow
1. `THOUGHT`: I need calendar data.
2. `ACTION`: `get_calendar("tomorrow")`
3. Orchestrator returns observation (`"9am"`).
4. `THOUGHT`: I now have the answer.
5. `ACTION`: `final_answer("9am")`

Prompt chaining links these actions, but chaining **alone** is not enough.

---

## 4) Output Validation: Gate Checks

LLMs can hallucinate, fail formats, or miss instructions. Early-step errors can cascade.

Gate checks add quality control between steps:

- **Pass**: continue.
- **Fail**: halt, retry, or retry with failure feedback.

### Generic pseudo-code

```python
output = call_llm(prompt_step1)

if validate_output(output):
	next_input = process(output)
	call_llm(prompt_step2, next_input)
else:
	handle_error(output)
```

### Typical failure strategies

1. **Stop** immediately (high-risk workflows).
2. **Retry** with same prompt.
3. **Retry with feedback** (include failure reason explicitly).

---

## 5) Types of Gate Checks

| Type | What it validates | Common implementation |
|---|---|---|
| **Format checks** | JSON/XML shape, required fields, length | Pydantic, schema validation, structured output APIs |
| **Content checks** | Keywords, citation presence, topical relevance | Regex, embedding similarity, secondary LLM checks |
| **Logic checks** | Numeric/logical consistency, code quality | `ast`, linters, unit tests, policy constraints |

---

## 6) Use Case: Data Analysis Script Generation

Goal: generate Python code that reads a CSV, computes average for a column, and writes output.

### Step 1 — Generate outline

Prompt asks for a short, numbered plan.

Optional **Gate 1**:
- list format present,
- key verbs present (`read`, `process`, `write`).

### Step 2 — Generate code from outline

Prompt injects `outline_response` from Step 1.

**Gate 2**:
- validate syntax via `ast.parse()` (or linter).

### Step 3 — Refine if syntax failed

Feed back generated code + syntax error details.

Re-run Gate 2 with max retry count.

### End-to-end chain

1. Prompt 1 → Outline → Gate 1
2. Prompt 2 → Code → Gate 2
3. If fail: Prompt 3 (fix) → Gate 2 (retry loop)

---

## 7) Implementing Prompt Chains in Python

At runtime, prompt chaining is string management + sequential API calls.

```python
prompt_step1 = """
You are a helpful programming assistant.
I need a Python script to read input_data.csv,
calculate the average of a column named 'value',
and write the result to output.txt.
Provide a simple step-by-step outline.
"""

outline_response = get_completion(prompt_step1)

prompt_step2 = f"""
Based on the outline below, write complete Python code.
Use standard libraries and include comments.

Outline:
---
{outline_response}
---
"""

code_response = get_completion(prompt_step2)
```

Syntax gate check:

```python
import ast

def check_python_syntax(code: str) -> tuple[bool, str]:
	try:
		ast.parse(code)
		return True, "No syntax errors found."
	except SyntaxError as e:
		return False, f"Syntax Error: {e}"
```

---

## 8) Pydantic for Reliable Structured Outputs

Natural language outputs vary in structure and are hard to automate safely.

Pydantic solves this with explicit schemas:

- **Validation**: rejects malformed or incomplete data.
- **Parsing**: converts JSON into typed Python objects.

### Why this matters in chains

Pydantic acts as a gate check between steps:

$$
	ext{LLM JSON} \xrightarrow{\text{Pydantic validate}} \text{Typed Object} \rightarrow \text{Next Step}
$$

### Example models: `OrderItem` and `Order`

```python
from pydantic import BaseModel, Field
from typing import List, Optional


class OrderItem(BaseModel):
	sku: str = Field(..., description="Stock Keeping Unit")
	quantity: int = Field(..., description="Quantity ordered")
	item_name: Optional[str] = Field(None, description="Item name if available")


class Order(BaseModel):
	order_id: int = Field(..., description="Unique order identifier")
	customer_email: Optional[str] = Field(None, description="Customer email")
	items: List[OrderItem] = Field(..., description="Order items")
	total_amount: float = Field(..., description="Order total amount")
```

### Validation gate

```python
from pydantic import ValidationError

def validate_order_payload(payload: dict) -> tuple[bool, str]:
	try:
		Order.model_validate(payload)
		return True, "Valid payload"
	except ValidationError as e:
		return False, e.json()
```

---

## 9) Practical Design Rules

1. Break large tasks into stage-specific prompts.
2. Define explicit success criteria per stage.
3. Add deterministic gate checks where possible.
4. Limit retries to avoid infinite loops.
5. Log prompt/output/validation per iteration.
6. Use structured outputs + Pydantic for machine-to-machine reliability.

---

## 10) Recap

- Task decomposition improves reasoning quality.
- Prompt chaining creates a programmable pipeline.
- Gate checks prevent error propagation.
- Pydantic makes agent outputs robust and interoperable.

These patterns form the backbone of reliable agentic workflows in production.
