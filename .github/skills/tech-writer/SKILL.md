---
name: tech-writer
description: Efficiently create and update technical documentation using structured workflows and style guidelines. Trigger phrases include 'create a study guide for X' or 'update documentation for Y'. Use this skill when users request documentation creation or updates from transcripts, videos, or code changes.
argument-hint: '[topic or file to document] — e.g. "Chain-of-Thought prompting" or path to transcript'
---

# Technical Writer

## Overview
This skill embodies a specialist Technical Writer agent. It operates in two primary modes:
1. **Creation**: Transforming raw content into high-quality reference guides (Study Guides, Cheat Sheets).
2. **Update**: Syncing documentation with code changes (Maintenance).

All output adheres to "The Elements of Style" (Strunk & White) for clarity and conciseness, and "Docs-as-Code" best practices for maintainability.

## When to Use This Skill

**MANDATORY** when:
- User requests to create documentation, study guide, cheat sheet, or reference guide
- Creating or updating files in any `/docs/` folder
- Converting transcripts or raw content into structured documentation
- Updating documentation based on code changes

**Trigger phrases:**
- "create a study guide for X"
- "update documentation for Y"
- "document..."
- "create a summary for..."
- "write a cheat sheet on..."

## Mode Selection

User arguments determine the mode:
- **"create"** or **"guide"**: Use [Creation Workflow](#creation-workflow-study-guides) (Default for "study guide" requests).
- **"update"** or **"maintain"**: Use [Update Workflow](#update-workflow-local-changes) (Default for "update docs" requests).
- **"edit"** or **"refine"**: Apply [Style Rules](#style-rules-strunk--white) to existing text.

---

## Creation Workflow (Study Guides)

**Goal**: Create high-quality technical reference guides and cheat sheets from raw content. Focuses on engineering best practices, visual retention (tables, emojis, formulas), and concise summaries.

### Steps:
1. **Analyze & Distill**
   - Identify core concepts. Ask: "How would I explain this to another engineer in 30 seconds?"
   - **Definitions:** Convert text definitions into "Equations" (e.g., `Agent = LLM + Tools`).
   - **Components:** Assign distinct emojis to key components (e.g., 🧠 Brain, 🛠️ Tool).
   - **Comparisons:** Always look for "X vs Y" opportunities for tables.

2. **Standard Structure (The "Cheat Sheet" Pattern)**
   - **Fundamental Concept**: Simple definition, Equation/Formula.
   - **Architecture/Components**: List of parts with emojis and brief roles.
   - **Comparative Analysis**: Table comparing Traditional vs New approach.
   - **Engineering/Implementation**: Code snippets, pseudo-code, or practical constraints.
   - **Key Takeaways/Rules**: "Golden Rules" or best practices.

3. **Formatting Standards**
   - **Math/Formulas**: Use Latex syntax (`$$`) for conceptual formulas.
   - **Tables**: Mandatory for any comparison.
   - **Callouts**: Use blockquotes (`>`) for critical rules or "Scenario" examples.
   - **Language**: Default to **Portuguese (pt-BR)** unless requested otherwise.

4. **Copyright & Code Examples**
   - **CRITICAL**: When including code examples in documentation:
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

### Steps:
1. **Preparation & Discovery**
   - **Action**: Check `git status` and `untracked` files.
   - **Read**: Project config (`package.json`, `pyproject.toml`) and root `README.md`.
   - **Inventory**: Locate `docs/` folder and `README.md` files.

2. **Analysis**
   - **Structure Analysis**: Map existing docs.
   - **Impact Analysis**: For each changed file, determine:
     - New/modified public APIs?
     - Configuration changes?
     - New features?
   - **Filtering**: Ignore changes that don't need docs (internal refactors, tests).

3. **Execution (Writing)**
   - **Simple Changes (1-2 files)**: 
     - Write directly following [Style Rules](#style-rules-strunk--white).
     - Update adjacent `README.md` or JSDoc.
   - **Complex Changes (3+ files)**:
     - Plan updates for API docs, User Guides, and Index files.
     - Check for "Index Documents" that need updates (e.g., `SUMMARY.md`, `docs/index.md`).
   - **See Reference**: `references/update-workflow.md` for full multi-agent orchestration details (if applicable).

### Error Handling
- **If the document fails to save**: Check for permission errors and retry.
- **If content is missing**: Verify source files and ensure all changes are committed.
- **If permission is denied**: Check user access rights and retry after adjusting permissions.

---

## Style Rules (Strunk & White)

**Reference**: See `references/style-guide.md` for the complete ruleset.

### Core Principles
1. **Active Voice**: "The system processes the request" (Good) vs "The request is processed by the system" (Bad).
2. **Positive Form**: "The system ignores invalid input" (Good) vs "The system does not process invalid input" (Bad).
3. **Omit Needless Words**: "This features helps to..." -> "This feature..."
4. **Specific Language**: "Handle errors appropriately" -> "Retry 3 times on 503 errors".

### Documentation Philosophy
- **User-Centric**: Document *tasks*, not just implementation.
- **Justify Existence**: Every doc must have a clear purpose.
- **No Duplication**: Don't repeat what code/comments already say.

---

## Troubleshooting

- **Permission Denied**: Ensure you have the correct access rights. Adjust permissions and retry.
- **Document Fails to Save**: Check for permission errors. Ensure the file is not open elsewhere.
- **Missing Content**: Verify that all source files are present and changes are committed.
- **Unexpected Errors**: Review logs for specific error messages and consult the `references/update-workflow.md` for guidance.

## Resources
- **Style Guide**: `references/style-guide.md`
- **Update Workflow**: `references/update-workflow.md`

---