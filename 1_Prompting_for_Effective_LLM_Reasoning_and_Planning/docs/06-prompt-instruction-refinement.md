```markdown
# Prompt Instruction Refinement

> **Definition:** The systematic process of evaluating and refining prompt instructions to align LLM outputs with user intent. It transforms interaction from trial-and-error to engineering.

$$
\text{Prompt}_{Optimized} = \sum (\text{Role} + \text{Task} + \text{Context} + \text{Format} + \text{Examples}) + \text{Iteration}
$$

---

## 🧩 Core Prompt Components

> (content omitted for brevity in this summary file — retained full guidance in the document)

---

## 🔄 Systematic Refinement Workflow

Effective refinement follows a strict feedback loop:

1.  **Initial Draft:** Write the base instruction.
2.  **Evaluate:** Execute and analyze output against expectations.
3.  **Isolate:** Pinpoint the failing component (e.g., wrong tone = Role; wrong structure = Format).
4.  **Adjust:** Modify *only* the identified component.
5.  **Iterate:** Repeat until convergence.

---

## 🚀 Conclusion
You now have a framework to:
1.  **Decompose** prompts into manageable components.
2.  **Iterate** systematically (one variable at a time).
3.  **Diagnose** failures by comparing Role, Task, Context, and Format.

> **Golden Rule:** Treat prompts as code. Version control, testing, and refactoring apply here just as they do in software engineering.

```
