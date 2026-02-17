---
name: create-study-guide
description: Create high-quality technical reference guides and cheat sheets from raw content. Focuses on engineering best practices, visual retention (tables, emojis, formulas), and concise summaries rather than verbatim transcription.
license: MIT
allowed-tools: [read_file, create_file, create_directory]
---

# Create Study Guide (Technical Reference)

## Overview
This skill transforms unstructured information (transcripts, notes, code) into **high-quality technical documentation** designed for quick reference and concept retention. The goal is to create a "Cheat Sheet" or "Engineering Guide," not just a summary.

## Design Philosophy
- **Reference over Reading:** The output should be scannable. Use it to *recall* concepts, not just to learn them for the first time.
- **Visual Retention:** Use emojis, tables, and formatting to create "mental anchors".
- **Engineering Mindset:** Use formulas, algorithms, and process flows to explain concepts.

## Workflow

### 1. Analyze & Distill
Identify core concepts. Ask: "How would I explain this to another engineer in 30 seconds?"
- **Definitions:** Convert text definitions into "Equations" (e.g., Agent = LLM + Tools).
- **Components:** Assign distinct emojis to key components (e.g., 🧠 Brain, 🛠️ Tool).
- **Comparisons:** Always look for "X vs Y" opportunities for tables.

### 2. Standard Structure (The "Cheat Sheet" Pattern)
1.  **Fundamental Concept**: Simple definition, Equation/Formula.
2.  **Architecture/Components**: List of parts with emojis and brief roles.
3.  **Comparative Analysis**: Table comparing Traditional vs New approach.
4.  **Engineering/Implementation**: Code snippets, pseudo-code, or practical constraints.
5.  **Key Takeaways/Rules**: "Golden Rules" or best practices.

### 3. Formatting Standards (Markdown)
- **Math/Formulas**: Use Latex syntax (`$$`) for conceptual formulas.
- **Tables**: Mandatory for any comparison.
- **Callouts**: Use blockquotes (`>`) for critical rules or "Scenario" examples.
- **Language**: Default to **Portuguese (pt-BR)** unless requested otherwise.

## Example Template

```markdown
# [Topic Name] - Reference Guide

## 1. Fundamental Concept

**Definition:** Brief, high-level explanation.

### Conceptual Formula
$$ \text{Concept} = \text{Component A} + \text{Component B} $$

---

## 2. Architecture & Components

*   **🧠 Component A:** Role description.
*   **⚙️ Component B:** Role description.
*   **🔌 Component C:** Role description.

---

## 3. Comparative Analysis

| Feature | Approach A (Old) | Approach B (New) |
| :--- | :--- | :--- |
| **Performance** | Low | High |
| **Use Case** | Batch | Real-time |

---

## 4. Engineering Patterns / Best Practices

### The [Pattern Name] Pattern
1.  **Step 1:** Action...
2.  **Step 2:** Action...

> **💡 Pro Tip:** Critical advice or "Golden Rule".
```
