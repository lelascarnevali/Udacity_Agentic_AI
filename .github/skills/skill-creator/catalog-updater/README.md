# Skill Catalog Updater (Utility)

This is a **utility script**, not a skill. It's integrated into the `skill-creator` workflow.

## Purpose

Automatically updates `.github/skills/README.md` by scanning all SKILL.md files and extracting their metadata.

## Usage

Run this script after creating, modifying, or deleting any skill:

```bash
.github/skills/skill-catalog-updater/update-catalog.sh
```

## What it does

1. Scans `.github/skills/` for all `SKILL.md` files
2. Extracts `name` and `description` from frontmatter
3. Generates updated `README.md` with all current skills
4. Adds timestamp

## Integration

This utility is called as part of the `skill-creator` workflow. See [skill-creator/SKILL.md](../skill-creator/SKILL.md) for details.

## Technical Details

- **Language**: Bash
- **Dependencies**: Standard Unix tools (find, awk, grep)
- **Output**: Overwrites `.github/skills/README.md`
- **Performance**: ~100ms for typical repos

---

*This is not a discoverable skill - it's a utility used by skill-creator.*
