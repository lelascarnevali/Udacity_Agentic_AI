# GitHub Copilot Instructions

This repository hosts Udacity Agentic AI exercises focused on effective prompting for LLM reasoning and planning. Keep guidance minimal, precise, and aligned with the actual workspace.

## 1. Repository Context
- Purpose: hands-on notebooks and lightweight utilities for LLM reasoning and planning.
- Stack: macOS + VS Code + Jupyter + Python.

## 2. Repository Structure
```
.
├── .github/                                   # Copilot configuration and support assets
│   └── skills/                                # Copilot "skills" docs and helper scripts
├── 1_Prompting_for_Effective_LLM_Reasoning_and_Planning/ # Module 1: Prompting foundations
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 2_Agentic_Workflows/                       # Module 2: Designing agentic workflows
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 3_Building_Agents/                         # Module 3: Implementing agents
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── 4_Multi-Agent_Systems/                     # Module 4: Multi-agent systems
│   ├── docs/                                  # Module notes, references, and reading materials
│   └── exercises/                             # Jupyter notebooks for hands-on practice
├── scripts/                                   # Reusable Python utilities for notebooks
└── .venv/                                     # Local Python virtual environment (optional)
```

## 3. Skills (skill.sh)
- integrate Copilot "skills" via a shell script.
- Skills location: `.github/skills/`.

## 3.1 Operating Workflow

### Skill-First with Memory Context (MANDATORY)
**BEFORE creating a plan or executing ANY non-trivial task:**

1. **Consult Knowledge Indices**:
   - **Skills Catalog**: Read `.github/skills/README.md` to identify what capabilities are available.
   - **Memory Index**: Read `.github/agents/memory/README.md` to identify what past learnings/preferences apply.

2. **Activate Specific Knowledge**:
   - Read the *specific* skill file found in the catalog (e.g., `SKILL.md`).
   - Read the *specific* memory file found in the index (e.g., `*-memory.md`).

3. **Plan & Execute**:
   - Create a plan (using `manage_todo_list`) that explicitly incorporates the steps/rules from the loaded skills and memory.
   - Execute the plan, adhering strictly to the loaded guidelines.

**Skip skill/memory check ONLY for:**
- Simple conversational responses
- Trivial single-line answers
- Tasks not involving file operations or workflows

### Execution Best Practices
- **Workflow:** Read Indices (`README.md`s) → Read Specific Files → Plan (`manage_todo_list`) → Execute.
- **File Editing Rule (MANDATORY):** NEVER use terminal commands (like `cat`, `echo`, `sed`) to create or edit files. ALWAYS use VS Code tools (`create_file`, `replace_string_in_file`, `edit_notebook_file`).
- Be specific with meaningful names (functions, variables, commit messages)
- Provide top-level context comments for complex implementations
- Use precise, domain-specific terms likely to appear in the codebase
- Execute changes minimally; bundle commits logically
- Only commit when explicitly asked or after confirmation

## 3.2 Language Policy
- Documentation, code comments, and prompt design: write in English.
- Chat responses to the user: reply in Portuguese (pt-BR).
- Keep examples consistent: internal artifacts in English; communication in Portuguese.


## 3.3 Garantindo a Consulta de Skills e Memórias (Aprimorado)

Para evitar inconsistências e garantir que as skills e memórias sejam consultadas corretamente, siga estas etapas adicionais:

1. **Validação Automática**:
   - Antes de executar qualquer tarefa, registre quais skills e memórias foram consultadas.
   - Inclua logs no formato:
     ```
     [Timestamp] Skill consultada: [NOME_DA_SKILL] | Memória consultada: [NOME_DA_MEMÓRIA]
     ```

2. **Exemplos Práticos**:
   - **Exemplo 1**: Consultar uma skill específica:
     ```
     Leia o arquivo `.github/skills/prompt-engineering/SKILL.md` para entender como otimizar prompts.
     ```
   - **Exemplo 2**: Consultar memórias relevantes:
     ```
     Leia o arquivo `.github/agents/memory/README.md` para identificar aprendizados prévios aplicáveis.
     ```

3. **Ações Corretivas**:
   - Caso uma skill ou memória não seja consultada, interrompa a execução e retorne ao fluxo correto.
   - Informe ao usuário que a consulta foi corrigida. Exemplo de mensagem:
     ```
     A consulta da skill/memória foi corrigida. Certifique-se de seguir o fluxo correto para evitar inconsistências futuras.
     ```

4. **Auditoria**:
   - Mantenha um registro das skills e memórias consultadas para referência futura.
   - Integre a validação com ferramentas de CI/CD para garantir conformidade automática.

Essas etapas garantem que o fluxo seja seguido rigorosamente e que todas as tarefas sejam executadas com base nas informações corretas.

## 4. Virtual Environment
- Preferred: local virtualenv at `.venv/`.
- Setup on macOS:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python --version
pip --version
```

- Deactivate:

```sh
deactivate
```

## 5. Standards
- Python: follow PEP 8; prefer type hints and concise docstrings; use `black`/`ruff` when applicable.
- Notebooks: write formulas in LaTeX within markdown cells.
  - Inline: `$E=mc^2$`
  - Block: `$$\int_a^b f(x)\,dx$$`

## 6. Context Transparency
At the end of each response, always include a section showing which resources were used:

```markdown
---
**Contexto utilizado:**
- **Skills:** [list of skills from .github/skills/ that were referenced.]
- **Arquivos:** [list of files that were read or modified]
- **Memória:** [agent memory files from .github/agents/memory/ if consulted]
```

Guidelines:
- Only list skills if explicitly consulted from `.github/skills/`
- List all files read with `read_file` or modified with editing tools
- Include memory files only if actually accessed
- Omit the section entirely for simple conversational responses that don't use external resources
- Keep the format concise and scannable

— End of instructions —
