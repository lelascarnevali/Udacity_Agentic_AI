---
name: skill-catalog-updater
description: Automatically updates the skills catalog (README.md) when skills are created or deleted. Scans .github/skills/ directory, extracts metadata from SKILL.md files, and regenerates the catalog with consistent formatting.
license: MIT
allowed-tools: Bash, File Operations
---

# Skill Catalog Updater

## Overview

Maintains an up-to-date catalog of all available skills by scanning the `.github/skills/` directory and automatically generating the `README.md` file with current skill information.

## When to Use

Use this skill when:
- A new skill has been created
- An existing skill has been deleted
- Skill metadata (name, description) has changed
- You want to refresh the skills catalog

## How It Works

1. **Scan Directory**: Searches `.github/skills/` for all `SKILL.md` files
2. **Extract Metadata**: Reads frontmatter (name, description) from each SKILL.md
3. **Categorize**: Groups skills by type (Development, Documentation, Management, etc.)
4. **Generate Catalog**: Creates formatted README.md with:
   - Quick reference section
   - Organized skill listings
   - Usage workflow
   - Directory structure
5. **Preserve Structure**: Maintains consistent formatting and organization

## Usage

### Basic Update

```bash
# Navigate to repository root
cd /path/to/repository

# Run the updater
.github/skills/skill-catalog-updater/update-catalog.sh
```

### After Creating a New Skill

```bash
# 1. Create your new skill
# 2. Ensure SKILL.md has proper frontmatter
# 3. Run updater
.github/skills/skill-catalog-updater/update-catalog.sh

# 4. Verify the catalog was updated
git diff .github/skills/README.md
```

### After Deleting a Skill

```bash
# 1. Delete the skill directory
rm -rf .github/skills/old-skill/

# 2. Run updater to remove from catalog
.github/skills/skill-catalog-updater/update-catalog.sh

# 3. Commit changes
git add .github/skills/
git commit -m "chore: remove old-skill and update catalog"
```

## Skill Frontmatter Requirements

For the updater to work correctly, each `SKILL.md` must have proper frontmatter:

```markdown
---
name: skill-name
description: Brief description of what the skill does and when to use it
license: MIT  # optional
allowed-tools: Bash, Python  # optional
---
```

### Required Fields

- **name**: Kebab-case identifier (e.g., `git-commit`, `skill-creator`)
- **description**: One-line summary of purpose and use cases

### Optional Fields

- **license**: License type (MIT, Apache-2.0, etc.)
- **allowed-tools**: Comma-separated list of tools the skill uses

## Catalog Structure

The generated catalog follows this organization:

```markdown
# Skills Catalog

## Quick Reference
[Brief introduction and usage note]

## Available Skills

### Category Name
#### skill-name
**Purpose:** [from description]
**Use when:** [extracted or inferred]
**Key features:** [bullets of main capabilities]
**Location:** [link to skill directory]

---

## Usage Workflow
[Step-by-step guide]

## Directory Structure
[Tree view of .github/skills/]

## Keeping This Catalog Updated
[Instructions for using this skill]
```

## Troubleshooting

### Catalog Not Updating

**Problem**: README.md not changed after running updater

**Solutions**:
1. Check that SKILL.md files have valid frontmatter
2. Verify you're running from repository root
3. Check file permissions: `chmod +x .github/skills/skill-catalog-updater/update-catalog.sh`
4. Review script output for errors

### Skill Not Appearing

**Problem**: New skill not showing in catalog

**Checklist**:
- [ ] SKILL.md file exists in skill directory
- [ ] Frontmatter has `name` and `description` fields
- [ ] Frontmatter is valid YAML (between `---` markers)
- [ ] Updater script was run after creating skill

### Formatting Issues

**Problem**: Catalog formatting looks incorrect

**Solutions**:
1. Review template in script matches expected format
2. Check for special characters in skill descriptions
3. Verify Markdown syntax in generated sections

## Best Practices

1. **Run after any skill changes**: Create, delete, or modify
2. **Commit catalog with skill**: Keep them in sync
3. **Review before committing**: Check generated content is accurate
4. **Use conventional commits**: When updating catalog
   ```bash
   git commit -m "docs: update skills catalog with new-skill"
   ```

## Integration with Copilot Instructions

The catalog is referenced in `.github/copilot-instructions.md`:

```markdown
## 3.1 Operating Workflow

### Skill-First Approach
**MANDATORY**: Before executing ANY task:
1. Check `.github/skills/README.md` for available skills
2. Search for relevant skill using the catalog
3. Follow skill's workflow instead of direct commands
```

This ensures Copilot always checks the catalog first before executing tasks.

## Technical Details

### Script Location
`.github/skills/skill-catalog-updater/update-catalog.sh`

### Dependencies
- `bash` (4.0+)
- `grep`, `sed`, `awk` (standard Unix tools)
- `find` (for directory scanning)

### Output
- Overwrites `.github/skills/README.md`
- Preserves git history (use `git diff` to review)

### Performance
- Fast: ~100ms for typical repos with <20 skills
- Scalable: Handles hundreds of skills efficiently

## Examples

### Example 1: Adding a New Skill

```bash
# Create new skill
mkdir -p .github/skills/database-migration
cat > .github/skills/database-migration/SKILL.md << 'EOF'
---
name: database-migration
description: Manage database schema migrations with version control and rollback capabilities
---
# Database Migration
[skill content...]
EOF

# Update catalog
.github/skills/skill-catalog-updater/update-catalog.sh

# Verify and commit
git add .github/skills/
git commit -m "feat: add database-migration skill

- Manage schema migrations
- Version control for database changes
- Rollback capabilities
- Update skills catalog"
```

### Example 2: Bulk Update After Multiple Changes

```bash
# After creating/modifying/deleting multiple skills
.github/skills/skill-catalog-updater/update-catalog.sh

# Review all changes
git diff .github/skills/README.md

# Commit together
git add .github/skills/
git commit -m "chore: reorganize skills and update catalog

- Add: new-skill-1, new-skill-2
- Update: existing-skill descriptions
- Remove: deprecated-skill
- Catalog reflects all changes"
```

## Maintenance

### Updating the Updater

If you need to modify how the catalog is generated:

1. Edit the script: `.github/skills/skill-catalog-updater/update-catalog.sh`
2. Test with dry-run: `bash -x update-catalog.sh` (see commands)
3. Verify output: Review generated README.md
4. Commit changes to both script and catalog

### Version History

Track updater changes in commits:
```bash
git log --oneline -- .github/skills/skill-catalog-updater/
```

---

**Note**: This skill is self-documenting. When updated, run itself to update the catalog!
