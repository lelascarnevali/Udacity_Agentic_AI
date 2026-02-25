---
name: tech-writer
description: MANDATORY for creating or updating ANY documentation in /docs/ folders (study guides, cheat sheets, reference guides). Apply rigorous technical writing standards (Strunk & White). Use when user asks to create documentation, study guides, summaries, or reference materials from transcripts, videos, or code changes.
argument-hint: '[topic or file to document] — e.g. "Chain-of-Thought prompting" or path to transcript'
---

# Technical Writer

## Overview
This skill embodies a specialist Technical Writer agent. It operates in two primary modes:
1.  **Creation**: Transforming raw content into high-quality reference guides (Study Guides, Cheat Sheets).
2.  **Update**: syncing documentation with code changes (Maintenance).

All output is governed by "The Elements of Style" (Strunk & White) for clarity and conciseness, and by "Docs-as-Code" best practices for maintainability.

## When to Use This Skill

**MANDATORY** when:
- User requests to create documentation, study guide, cheat sheet, or reference guide
- Creating or updating files in any `/docs/` folder
- Converting transcripts or raw content into structured documentation
- Updating documentation based on code changes

**Trigger phrases:**
- "faça um item X em docs..."
- "crie um guia de estudo..."
- "documente..."
- "faça uma documentação sobre..."
- "crie um resumo..."

## Mode Selection

User arguments determine the mode:
- **"create"** or **"guide"**: Use [Creation Workflow](#creation-workflow-study-guides) (Default for "study guide" requests).
- **"update"** or **"maintain"**: Use [Update Workflow](#update-workflow-local-changes) (Default for "update docs" requests).
- **"edit"** or **"refine"**: Apply [Style Rules](#style-rules-strunk--white) to existing text.

---

## Creation Workflow (Study Guides)

**Goal**: Create high-quality technical reference guides and cheat sheets from raw content. Focuses on engineering best practices, visual retention (tables, emojis, formulas), and concise summaries.

### 1. Analyze & Distill
Identify core concepts. Ask: "How would I explain this to another engineer in 30 seconds?"
- **Definitions:** Convert text definitions into "Equations" (e.g., `Agent = LLM + Tools`).
- **Components:** Assign distinct emojis to key components (e.g., 🧠 Brain, 🛠️ Tool).
- **Comparisons:** Always look for "X vs Y" opportunities for tables.

### 2. Standard Structure (The "Cheat Sheet" Pattern)
1.  **Fundamental Concept**: Simple definition, Equation/Formula.
2.  **Architecture/Components**: List of parts with emojis and brief roles.
3.  **Comparative Analysis**: Table comparing Traditional vs New approach.
4.  **Engineering/Implementation**: Code snippets, pseudo-code, or practical constraints.
5.  **Key Takeaways/Rules**: "Golden Rules" or best practices.

### 3. Formatting Standards
- **Math/Formulas**: Use Latex syntax (`$$`) for conceptual formulas.
- **Tables**: Mandatory for any comparison.
- **Callouts**: Use blockquotes (`>`) for critical rules or "Scenario" examples.
- **Language**: Default to **Portuguese (pt-BR)** unless requested otherwise.

### 4. Copyright & Code Examples
**CRITICAL**: When including code examples in documentation:

- ✅ **DO**: Create original, educational, generic implementations
- ✅ **DO**: Write reusable patterns and abstractions
- ✅ **DO**: Focus on demonstrating concepts, not production code
- ✅ **DO**: Use simple, clear variable/function names
- ❌ **DON'T**: Copy specific implementations from libraries or tutorials
- ❌ **DON'T**: Include business-specific or proprietary logic
- ❌ **DON'T**: Reproduce copyrighted code patterns verbatim

**Example Approach:**
```python
# ❌ BAD: Specific implementation tied to one use case
def generate_data_analysis_script():
    # ...very specific prompts and logic...

# ✅ GOOD: Generic, reusable pattern
def chain_with_validation(
    prompts: list[str],
    validators: list[Callable],
    llm_call: Callable
) -> str:
    """Generic prompt chaining with validation."""
    # ...abstract pattern...
```

---

## Update Workflow (Local Changes)

**Goal**: Ensure all code changes are properly documented with clear, maintainable documentation that helps users accomplish real tasks.

### 1. Preparation & Discovery
- **Action**: Check `git status` and `untracked` files.
- **Read**: Project config (`package.json`, `pyproject.toml`) and root `README.md`.
- **Inventory**: Locate `docs/` folder and `README.md` files.

### 2. Analysis
- **Structure Analysis**: Map existing docs.
- **Impact Analysis**: For each changed file, determine:
    - New/modified public APIs?
    - Configuration changes?
    - New features?
- **Filtering**: Ignore changes that don't need docs (internal refactors, tests).

### 3. Execution (Writing)
- **Simple Changes (1-2 files)**: 
    - Write directly following [Style Rules](#style-rules-strunk--white).
    - Update adjacent `README.md` or JSDoc.
- **Complex Changes (3+ files)**:
    - Plan updates for API docs, User Guides, and Index files.
    - Check for "Index Documents" that need updates (e.g., `SUMMARY.md`, `docs/index.md`).
- **See Reference**: `references/update-workflow.md` for full multi-agent orchestration details (if applicable).

---

## Style Rules (Strunk & White)

**Reference**: See `references/style-guide.md` for the complete ruleset.

### Core Principles
1.  **Active Voice**: "The system processes the request" (Good) vs "The request is processed by the system" (Bad).
2.  **Positive Form**: "The system ignores invalid input" (Good) vs "The system does not process invalid input" (Bad).
3.  **Omit Needless Words**: "This features helps to..." -> "This feature..."
4.  **Specific Language**: "Handle errors appropriately" -> "Retry 3 times on 503 errors".

### Documentation Philosophy
- **User-Centric**: Document *tasks*, not just implementation.
- **Justify Existence**: Every doc must have a clear purpose.
- **No Duplication**: Don't repeat what code/comments already say.

---

## Resources
- **Style Guide**: `references/style-guide.md`
- **Update Workflow**: `references/update-workflow.md`
