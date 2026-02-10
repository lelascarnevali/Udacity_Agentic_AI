#!/usr/bin/env bash

# Skill Catalog Updater
# Automatically generates .github/skills/README.md from all SKILL.md files

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SKILLS_DIR="${REPO_ROOT}/.github/skills"
CATALOG_FILE="${SKILLS_DIR}/README.md"

echo "🔄 Updating Skills Catalog"
echo "📂 Skills directory: $SKILLS_DIR"

# Find all SKILL.md files
SKILLS=$(find "$SKILLS_DIR" -name "SKILL.md" -type f | sort)

if [ -z "$SKILLS" ]; then
    echo "⚠️  No SKILL.md files found"
    exit 1
fi

COUNT=$(echo "$SKILLS" | wc -l | tr -d ' ')
echo "✅ Found $COUNT skill(s)"

# Start generating catalog
cat > "$CATALOG_FILE" << 'EOF'
# Skills Catalog

This directory contains specialized skills that extend Copilot's capabilities with domain-specific knowledge, workflows, and tools.

## 📋 Quick Reference

**Always check this catalog before executing tasks** - skills provide validated, tested procedures that should be used instead of direct commands.

## 🛠️ Available Skills

EOF

# Process each skill
echo "$SKILLS" | while read -r SKILL_FILE; do
    SKILL_DIR=$(dirname "$SKILL_FILE")
    SKILL_NAME=$(basename "$SKILL_DIR")
    
    # Extract name and description from frontmatter
    NAME=$(awk '/^name:/ {sub(/^name: */, ""); gsub(/"/, ""); print; exit}' "$SKILL_FILE")
    DESC=$(awk '/^description:/ {sub(/^description: */, ""); gsub(/^["'\'']|["'\'']$/, ""); print; exit}' "$SKILL_FILE")
    
    # Use directory name if frontmatter name not found
    [ -z "$NAME" ] && NAME="$SKILL_NAME"
    [ -z "$DESC" ] && DESC="No description available"
    
    # Add to catalog
    cat >> "$CATALOG_FILE" << SKILL_ENTRY

### \`$NAME\`

**Description:** $DESC

**Location:** [.github/skills/$SKILL_NAME/](.github/skills/$SKILL_NAME/)

SKILL_ENTRY

done

# Add footer
CURRENT_DATE=$(date '+%Y-%m-%d %H:%M:%S')

cat >> "$CATALOG_FILE" << EOF

---

## 🚀 Usage Workflow

1. **Check this catalog** before starting any task
2. **Search for relevant skill** using semantic search or keywords
3. **Read the skill's SKILL.md** for detailed instructions
4. **Follow the skill's workflow** instead of using direct commands
5. **Trust the skill** - they contain validated, tested procedures

## 🔄 Keeping This Catalog Updated

This catalog is **automatically maintained** by the catalog updater utility (not a skill).

**To update:** Run \`.github/skills/skill-catalog-updater/update-catalog.sh\`

This is integrated into the \`skill-creator\` workflow - see that skill for details.

---

*Last updated: $CURRENT_DATE*
EOF

echo "✅ Catalog updated: $CATALOG_FILE"
echo ""
echo "📝 Review changes with: git diff .github/skills/README.md"

