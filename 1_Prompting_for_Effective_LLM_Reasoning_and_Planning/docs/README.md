# Module 1: Prompting for Effective LLM Reasoning and Planning

## Documentation Index

This module covers foundational techniques for prompting Large Language Models (LLMs) to reason and plan effectively within agentic workflows. Filenames are zero-padded to ensure correct ordering on GitHub.

### 🧠 Conceptual Foundations
Reference guides dealing with the theoretical aspects of prompt engineering.

- **[01. The Role of Prompting in Agentic AI](./01-the-role-of-prompting-in-agentic-ai.md)**
  *Understanding the "Agente = Perceber + Decidir + Agir" equation and the role of LLMs as the cognitive engine.*

- **[02. Role-Based Prompting: Engineering Guide](./02-role-based-prompting.md)**
  *Deep dive into the Persona Equation ($P(\\text{Response} | \\\\text{Context}, \\\\text{Role}, \\\\text{Constraints})$) and how identity shapes model output.*

- **[03. Implementing Role-Based Prompting](./03-implementing-role-based-prompting.md)**
  *From "Creative Actors" to "Professional Experts" — implementation patterns and examples in Python.*

- **[04. Chain-of-Thought & ReAct Frameworks](./04-chain-of-thought-and-react-prompting.md)**
  *Comparison of reasoning methods: CoT (internal chain-of-thought) vs ReAct (reasoning + acting with tools).*

- **[05. Applying CoT & ReAct with Python](./05-applying-cot-and-react-with-python.md)**
  *Code-first patterns for building Think/Act/Observe loops and safely parsing LLM actions.*

- **[06. Prompt Instruction Refinement](./06-prompt-instruction-refinement.md)**
  *Methodology for iteratively debugging and optimizing prompts using the Refinement Cycle.*

- **[07. Applying Prompt Refinement with Python](./07-applying-prompt-instruction-refinement-with-python.md)**
  *Practical examples of turning vague user input into structured, machine-readable outputs.*

- **[08. Chaining Prompts for Agentic Reasoning](./08-chaining-prompts-for-agentic-reasoning.md)**
  *Integrated guide covering chaining architecture, gate checks, Python implementation, and Pydantic-based structured validation.*

- **[09. LLM Feedback Loops](./09-llm-feedback-loops.md)**
  *Designing iterative feedback and evaluation loops for model improvement.*

---

### 🐍 Practical Tools & Examples
Supplemental code, snippets and best-practice patterns used across exercises.

- **Code examples:** see the individual guides above (03, 05, 07, 08, 09) for runnable snippets.
- **Validation patterns:** `ast` checks for syntax, `pydantic` for structured output validation, and regex-based parsers for ACT/OBS patterns.

---

If you find a broken link after the recent renames, please open an issue or submit a PR updating references elsewhere in the repository.
