# Update Documentation Workflow

## Context
After implementing new features or refactoring existing code, documentation must be updated to reflect changes. This skill orchestrates automated documentation updates using specialized tech-writer agents and parallel analysis.

## Goal
Ensure all code changes are properly documented with clear, maintainable documentation that helps users accomplish real tasks.

## Workflow Steps

### Preparation

1. **Read SADD skill if available**
   - If available, read the SADD skill to understand best practices for managing agents

2. **Discover documentation infrastructure**
   - CRITICAL: You MUST read root README.md and project config (package.json, pyproject.toml, etc.)
   - Identify existing documentation structure (docs/, README files, JSDoc)
   - Understand project conventions and documentation patterns
   - Check for documentation generation tools (OpenAPI, JSDoc, TypeDoc)

3. **Inventory existing documentation**
   - Find all documentation files
   - Check for generated docs

### Analysis

Do steps 4-5 in parallel using haiku agents:

4. **Analyze documentation structure**
   - Map existing documentation
   - Identify docs/ folder structure and organization
   - Find all README.md files and their purposes
   - Locate API documentation (generated or manual)
   - Note JSDoc/TSDoc patterns in codebase

5. **Analyze local changes**
   - Run `git status -u` to identify all changed files (including untracked)
     - If no uncommitted changes, run `git show --name-status` for latest commit
   - Filter to identify documentation-impacting changes:
     - New/modified public APIs
     - Changed module structures
     - Updated configuration options
     - New features or workflows
   - Launch separate haiku agents per changed file to:
     - Analyze the file and its documentation impact
     - Identify what documentation needs to be created/updated
     - Identify index documents that need updates
     - Prepare short summary of documentation requirements
   - Extract list of documentation tasks

### Documentation Planning

6. **Group changes by documentation area**
   - Aggregate analysis results
   - Group changes that can be covered by same documentation update:
     - **API Documentation**: All API changes → single agent
     - **Module READMEs**: Changes in same module → single agent
     - **User Guides**: Related feature changes → single agent
     - **JSDoc/Code Comments**: Complex logic changes → per-file agents
     - **Index Documents**: Updates to navigation and discovery docs → single agent
   - Identify index documents requiring updates:
     - Root `README.md`
     - Module `README.md`
     - `docs/` index files
   - Create documentation task assignments

### Documentation Writing

#### Simple Change Flow (1-2 files, minor updates)

If changes are simple, write documentation yourself following this guideline:

1. Read Tech Writer Agent guidelines from @/plugins/sdd/agents/tech-writer.md
2. Review the changed files and understand the impact
3. Identify which documentation needs updates
4. Make targeted updates following project conventions
5. Verify all links and examples work
6. Ensure documentation serves real user needs

#### Multi-Agent Flow (3+ files or significant changes)

If there are multiple changed files or significant documentation needs, use specialized agents:

7. **Launch `doc-analysis` agents (parallel)** (Haiku models)
   - Launch one analysis agent per documentation area identified
   - Provide each agent with:
     - **Context**: What changed in related files (git diff)
     - **Target**: Which documentation area to analyze
     - **Resources**: Existing documentation in that area
     - **Goal**: Create detailed documentation requirements
     - **Output**: Specific documentation tasks with priorities

8. **Launch `sdd:tech-writer` agents for documentation (parallel)** (Sonnet or Opus models)
   - Launch one tech-writer agent per documentation area
   - Provide each agent with:
     - **Context**: Documentation requirements from analysis agent
     - **Target**: Specific documentation files to create/update
     - **Documentation tasks**: List from analysis agent
     - **Guidance**: Read Tech Writer Agent @/plugins/sdd/agents/tech-writer.md for best practices
     - **Resources**: Existing documentation for style reference
     - **Goal**: Create/update comprehensive documentation

9. **Launch quality review agents (parallel)** (Sonnet or Opus models)
   - Launch `sdd:tech-writer` agents again for quality review
   - Provide:
     - **Context**: Original changes + new documentation created
     - **Goal**: Verify documentation quality and completeness
     - **Review criteria**:
       - All user-facing changes are documented
       - Code examples are accurate and work
       - Links and references are valid
       - Documentation follows project conventions
       - No unnecessary documentation bloat
     - **Output**: PASS confirmation or list of issues to fix

10. **Iterate if needed**
    - If any documentation areas have quality issues: Return to step 8
    - Launch new tech-writer agents only for areas with gaps
    - Provide specific instructions on what needs fixing
    - Continue until all documentation passes quality review

11. **Final verification**
    - Review all documentation changes holistically
    - Verify cross-references between documents work
    - Ensure no conflicting information
    - Confirm documentation structure is navigable

## Core Documentation Philosophy

### The Documentation Hierarchy

```text
CRITICAL: Documentation must justify its existence
├── Does it help users accomplish real tasks? → Keep
├── Is it discoverable when needed? → Improve or remove  
├── Will it be maintained? → Keep simple or automate
└── Does it duplicate existing docs? → Remove or consolidate
```

### What TO Document ✅

**User-Facing Documentation:**

- **Getting Started**: Quick setup, first success in <5 minutes
- **How-To Guides**: Task-oriented, problem-solving documentation  
- **API References**: When manual docs add value over generated
- **Troubleshooting**: Common real problems with proven solutions
- **Architecture Decisions**: When they affect user experience

**Developer Documentation:**

- **Contributing Guidelines**: Actual workflow, not aspirational
- **Module READMEs**: Navigation aid with brief purpose statement
- **Complex Business Logic**: JSDoc for non-obvious code
- **Integration Patterns**: Reusable examples for common tasks

### What NOT to Document ❌

**Documentation Debt Generators:**

- Generic "Getting Started" without specific tasks
- API docs that duplicate generated/schema documentation  
- Code comments explaining what the code obviously does
- Process documentation for processes that don't exist
- Architecture docs for simple, self-explanatory structures
- Changelogs that duplicate git history
- Documentation of temporary workarounds
- Multiple READMEs saying the same thing

**Red Flags - Stop and Reconsider:**

- "This document explains..." → What task does it help with?
- "As you can see..." → If it's obvious, why document it?
- "TODO: Update this..." → Will it actually be updated?
- "For more details see..." → Is the information where users expect it?

## Documentation Discovery Process

### Codebase Analysis

<mcp_usage>
Use Context7 MCP to gather accurate information about:

- Project frameworks, libraries, and tools in use
- Existing API endpoints and schemas  
- Documentation generation capabilities
- Standard patterns for the technology stack
</mcp_usage>

**Inventory Existing Documentation:**

```bash
# Find all documentation files
find . -name "*.md" -o -name "*.rst" -o -name "*.txt" | grep -E "(README|CHANGELOG|CONTRIBUTING|docs/)"

# Find index documents specifically
find . -name "index.md" -o -name "SUMMARY.md" -o -name "_sidebar.md" -o -name "getting-started.md"
find . -name "mkdocs.yml" -o -name "docusaurus.config.js"

# Check for generated docs
find . -name "openapi.*" -o -name "*.graphql" -o -name "swagger.*"

# Look for JSDoc/similar
grep -r "@param\|@returns\|@example" --include="*.js" --include="*.ts"
```

### User Journey Mapping

Identify critical user paths:

- **Developer onboarding**: Clone → Setup → First contribution
- **API consumption**: Discovery → Authentication → Integration
- **Feature usage**: Problem → Solution → Implementation
- **Troubleshooting**: Error → Diagnosis → Resolution

### Documentation Gap Analysis

**High-Impact Gaps** (address first):

- Missing setup instructions for primary use cases
- API endpoints without examples
- Error messages without solutions
- Complex modules without purpose statements

**Low-Impact Gaps** (often skip):

- Minor utility functions without comments
- Internal APIs used by single modules
- Temporary implementations
- Self-explanatory configuration
