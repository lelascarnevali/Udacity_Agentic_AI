#!/usr/bin/env python3
"""
Generate a BMAD-style agent memory entry in .github/agents/memory.

Usage examples:
  python scripts/new_memory_entry.py --context "readme scope" --topic "README scope and agent memory" --tags memory conventions bmad --source "repo workflow" --agent github-copilot --yaml

This creates: .github/agents/memory/readme-scope-agent-memory.md
"""
import argparse
import datetime
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MEMORY_DIR = REPO_ROOT / ".github" / "agents" / "memory"
TEMPLATE_PATH = MEMORY_DIR / "templates" / "bmad-template.md"


def kebab_case(text: str) -> str:
    # Lowercase, replace non-alphanum with hyphens, collapse, strip
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def build_frontmatter(agent: str, date: str, topic: str, tags: list[str], source: str) -> str:
    tags_yaml = "[" + ", ".join(f"'{t}'" for t in tags) + "]" if tags else "[]"
    fm = [
        "---",
        f"agent: {agent}",
        f"date: {date}",
        f"topic: {topic}",
        f"tags: {tags_yaml}",
        f"source: {source}",
        "---",
        "",
    ]
    return "\n".join(fm)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate BMAD-style memory entry")
    parser.add_argument("--context", required=True, help="Context for filename (kebab-cased)")
    parser.add_argument("--topic", default="", help="Concise topic title")
    parser.add_argument("--tags", nargs="*", default=[], help="Optional tags list")
    parser.add_argument("--source", default="", help="Optional source description")
    parser.add_argument("--agent", default="github-copilot", help="Agent name in frontmatter")
    parser.add_argument("--date", default=datetime.date.today().isoformat(), help="ISO date")
    parser.add_argument("--yaml", action="store_true", help="Include YAML frontmatter")
    args = parser.parse_args()

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    context_slug = kebab_case(args.context)
    if not context_slug:
        print("Error: context produced empty slug", file=sys.stderr)
        return 2

    out_path = MEMORY_DIR / f"{context_slug}-agent-memory.md"
    if out_path.exists():
        print(f"Error: target already exists: {out_path}", file=sys.stderr)
        return 3

    # Load template
    if TEMPLATE_PATH.exists():
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    else:
        # Fallback minimal template
        template = (
            "# Agent Memory Entry\n\n"
            "- **Date:** {{DATE}}\n"
            "- **Topic:** {{TOPIC}}\n"
            "- **Topics/Tags:** {{TAGS}}\n"
            "- **Source:** {{SOURCE}}\n\n"
            "## Context\n\n## Key Insights\n\n## Decisions / Rules\n\n## References\n\n## Next Actions\n\n"
        )

    # Replace tokens
    tags_line = ", ".join(args.tags) if args.tags else ""
    rendered = (
        template.replace("{{DATE}}", args.date)
        .replace("{{TOPIC}}", args.topic)
        .replace("{{TAGS}}", tags_line)
        .replace("{{SOURCE}}", args.source)
    )

    content_parts = []
    if args.yaml:
        content_parts.append(
            build_frontmatter(args.agent, args.date, args.topic, args.tags, args.source)
        )
    content_parts.append(rendered)
    content = "\n".join(content_parts)

    out_path.write_text(content, encoding="utf-8")
    print(f"Created: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
