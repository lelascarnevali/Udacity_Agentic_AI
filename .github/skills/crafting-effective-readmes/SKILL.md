---
name: crafting-effective-readmes
description: Provides templates and guidance for writing or improving README files for various projects. Use when you need to create, update, or review README files. Trigger phrases include 'How do I write a README for my open source project?' and 'What should I include in my personal project README?' Key capabilities include providing templates, identifying essential sections, and offering troubleshooting advice.
argument-hint: '[path/to/README.md or module name]'
---

# Crafting Effective READMEs

## Overview

READMEs are crucial for effectively communicating project details to your audience. Different audiences require different information. For example, a contributor to an open-source project needs different context than a future-you opening a config folder.

**Always ask:** Who will read this, and what do they need to know?

## Process

### Step 1: Identify the Task

**Ask:** "What README task are you working on?"

| Task | When |
|------|------|
| **Creating** | New project, no README yet |
| **Adding** | Need to document something new |
| **Updating** | Capabilities changed, content is stale |
| **Reviewing** | Checking if README is still accurate |

### Step 2: Task-Specific Questions

**Creating initial README:**
1. What type of project? (see Project Types in references)
2. What problem does this solve in one sentence?
3. What's the quickest path to "it works"?
4. Anything notable to highlight?

**Adding a section:**
1. What needs documenting?
2. Where should it go in the existing structure?
3. Who needs this info most?

**Updating existing content:**
1. What changed?
2. Read current README, identify stale sections
3. Propose specific edits

**Reviewing/refreshing:**
1. Read current README
2. Check against actual project state (package.json, main files, etc.)
3. Flag outdated sections
4. Update "Last reviewed" date if present

### Step 3: Always Ask

After drafting, ask: **"Anything else to highlight or include that I might have missed?"**

## Essential Sections (All Types)

Every README needs at minimum:

1. **Name** - Self-explanatory title
2. **Description** - What + why in 1-2 sentences  
3. **Usage** - How to use it (examples help)

## Input/Output Examples

**Example Input:**
- "How do I write a README for my open source project?"

**Example Output:**
- A structured README with sections: Install, Usage, Contributing, License.

**Example Input:**
- "What should I include in my personal project README?"

**Example Output:**
- A README with sections: What it does, Tech stack, Learnings.

## References

- For detailed guidance on section inclusion, see [section-checklist.md](path/to/section-checklist.md)
- `style-guide.md` - Common README mistakes and prose guidance
- `using-references.md` - Guide to deeper reference materials

## Troubleshooting

- **If the README is not clear:** Add more examples or consult the `style-guide.md` for common mistakes.
- **If sections are missing:** Refer to `section-checklist.md` to ensure all necessary parts are included.
- **If the README is outdated:** Follow the steps in the "Updating existing content" section to refresh it.
- **If the README lacks clarity:** Add examples or consult the `style-guide.md` for common mistakes.
- **If the README is missing sections:** An error message should indicate which sections are missing based on the checklist.

---