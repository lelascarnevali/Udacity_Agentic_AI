# Module 1: Prompting for Effective LLM Reasoning and Planning

## Documentation Index

This module covers the foundational techniques for prompting Large Language Models (LLMs) to reason and plan effectively within Agentic workflows.

### 🧠 Conceptual Foundations
Reference guides dealing with the theoretical aspects of prompt engineering.

- **[1. The Role of Prompting in Agentic AI](./1-the-role-of-prompting-in-agentic-ai.md)**  
  *Understanding the "Agente = Perceber + Decidir + Agir" equation and the role of LLMs as the cognitive engine.*

- **[2. Role-Based Prompting: Engineering Guide](./2-role-based-prompting.md)**  
  *Deep dive into the Persona Equation ($P(\text{Response} | \text{Context}, \text{Role}, \text{Constraints})$) and how identity shapes model output.*

- **[4. Chain-of-Thought & ReAct Frameworks](./4-chain-of-thought-and-react-prompting.md)**  
  *Comparison of reasoning methods: CoT (Internal Monologue) vs ReAct (Reasoning + Acting with Tools).*

- **[6. Prompt Instruction Refinement](./6-prompt-instruction-refinement.md)**  
  *Methodology for iteratively debugging and optimizing prompts using the Refinement Cycle.*

- **[8. Chaining Prompts for Agentic Reasoning](./8-chaining-prompts-for-agentic-reasoning.md)**  
  *Breaking complex tasks into sequential steps with validation gates for reliable multi-stage LLM workflows.*

---

### 🐍 Practical Implementation (Python)
Code-first guides for implementing these concepts using Python.

- **[3. Implementing Role-Based Prompting](./3-implementing-role-based-prompting.md)**  
  *From "Creative Actors" to "Professional Experts". Implementing the Persona Spectrum in code.*

- **[5. Applying CoT & ReAct with Python](./5-applying-cot-and-react-with-python.md)**  
  *Building the "Think/Act/Observe" loop and parsing LLM actions using Regex.*

- **[7. Applying Prompt Refinement with Python](./7-applying-prompt-instruction-refinement-with-python.md)**  
  *Structuring interaction loops to turn vague inputs into precise, programmable instructions.*
