---
name: skill-creator
description: Guides users in creating or updating skills when asked, e.g., 'How do I create a new skill?' or 'Help me update an existing skill'.
argument-hint: '[skill name] — e.g. "code-review" or "deploy-staging"'
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?"

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

- **High freedom**: Use when multiple approaches are valid.
- **Medium freedom**: Use when a preferred pattern exists.
- **Low freedom**: Use when operations are fragile and error-prone.

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
└── Bundled Resources (optional)
    ├── scripts/
    ├── references/
    └── assets/
```

#### SKILL.md (required)

Contains:

- **Frontmatter** (YAML): `name` and `description` fields.
- **Body** (Markdown): Instructions for using the skill.

#### Bundled Resources (optional)

- **Scripts**: Executable code for deterministic tasks.
- **References**: Documentation for context.
- **Assets**: Files used in output.

### Maintaining the Skills Catalog

After creating, modifying, or deleting a skill, update the skills catalog:

```bash
.github/skills/skill-creator/catalog-updater/update-catalog.sh
```

## Skill Creation Process

Skill creation involves these steps:

1. **Understand the Skill with Concrete Examples**: Understand how the skill will be used through examples. For instance, when building an image-editor skill, ask questions like:
   - "What functionality should the image-editor skill support?"
   - "Can you give examples of how this skill would be used?"

2. **Plan Reusable Skill Contents**: Analyze examples to determine reusable resources:
   - Scripts for repeated code.
   - References for documentation.
   - Assets for templates or files.

3. **Initialize the Skill**: Run the `init_skill.py` script to create a new skill directory:
   ```bash
   scripts/init_skill.py <skill-name> --path <output-directory>
   ```

4. **Edit the Skill**: Include beneficial information for Claude. Start with reusable resources and update SKILL.md.

5. **Package the Skill**: Package the skill into a .skill file:
   ```bash
   scripts/package_skill.py <path/to/skill-folder>
   ```

6. **Iterate**: Use the skill on real tasks, identify improvements, and update as needed.

### Troubleshooting

- **Validation Errors**: Check YAML frontmatter and directory structure.
- **Skill Not Triggering**: Ensure description includes specific trigger phrases.
- **Script Errors**: Test scripts independently.
- **Resource Loading Issues**: Verify references and assets are correctly linked.