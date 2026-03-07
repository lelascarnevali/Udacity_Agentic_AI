# AI Agent Instructions

> Udacity Agentic AI — notebooks e utilitários para raciocínio e planejamento com LLMs.
> **Single source of truth** para Claude Code, GitHub Copilot, Cursor, etc.
> Stack: macOS · VS Code · Jupyter · Python.

---

## 1. Workflow Obrigatório

### Step 0 — Context Analysis (executa em todo prompt, sem exceção)

> Skills e memórias vêm **exclusivamente** de `.github/skills/` e `.github/agents/memory/`. Ignore fontes externas (`~/.claude/projects/`, Copilot workspace, etc.).

1. Leia `.github/skills/README.md` e `.github/agents/memory/README.md`.
2. Identifique skills e memórias relevantes; leia seus arquivos se aplicável.
3. Inicie toda resposta não-trivial com uma seção **"Context Analysis"** listando o que foi encontrado. Omitir é erro crítico.

### Step 1 — ReAct Loop

- Construa um plano com a **native task management tool** antes de agir (obrigatório para 3+ passos ou decisões arquiteturais). Valide com o usuário antes de implementar.
- Loop: **Analyze → Decide → Act → Observe → Reflect** — atualize a lista de tarefas a cada micro-atividade.
- Nunca marque tarefa completa sem provar que funciona.
- **Subagent Strategy:** use subagentes sempre que possível para manter o contexto principal limpo. Delegue pesquisa, exploração e análise paralela a subagentes. Para problemas complexos, use mais subagentes para mais capacidade de processamento. Um foco por subagente.
- Para mudanças não-triviais, pergunte: "Existe uma solução mais elegante?"
- Bug reports: corrija diretamente — aponte logs/erros/testes e resolva.
- Após qualquer correção do usuário, registre o padrão em `.github/agents/memory/` via skill `agent-memory`.

### Regras de Edição (MANDATORY)

- **NUNCA** use comandos de terminal (`cat`, `echo`, `sed`, `awk`) para criar ou editar arquivos. Use sempre as **native file tools** (ver `CLAUDE.md`).

---

## 2. Commit Policy (MANDATORY)

1. Consulte a skill `git-commit` em `.github/skills/git-commit/SKILL.md` antes de qualquer commit.
2. Prefira `scripts/commit_with_skill.py` para automação.
3. Antes de gerar a mensagem, rode `git diff --staged` (ou `git diff`) e baseie a mensagem no diff real.
4. Sem operações destrutivas (force push, hard reset) sem aprovação explícita do usuário.
5. Só commite quando explicitamente solicitado.

---

## 3. Skills & Memory

- **Skills:** `.github/skills/` — catálogo em `.github/skills/README.md`.
- **Memory:** `.github/agents/memory/` — índice em `.github/agents/memory/README.md`. Arquivos registram *o que foi aprendido*, não procedimentos.
- **Onde colocar novo conhecimento:** `.github/instructions/workflow-architecture.instructions.md`.

---

## 4. Padrões

**Linguagem:** `docs/` em pt-BR · código/comentários em inglês · respostas ao usuário em pt-BR.

**Python:** PEP 8, type hints, docstrings concisos, `black`/`ruff`.

**Notebooks:** fórmulas em LaTeX — inline `$…$`, bloco `$$…$$`.

**Ambiente:** `.venv/` na raiz — detalhes em `.github/instructions/python-env.instructions.md`.

---

## 5. Core Principles

- **Simplicity First** — mudança mínima necessária. Sem over-engineering.
- **No Laziness** — encontre a causa raiz. Sem patches temporários.
- **Minimal Impact** — toque só o necessário. Evite regressões.

---

## 6. Context Transparency

Encerre toda resposta não-trivial com:

> **Contexto utilizado:** **Skills:** … | **Arquivos:** … | **Memória:** …

---

*Mapeamento de ferramentas: `CLAUDE.md` (Claude Code) · `.github/copilot-instructions.md` (Copilot).*
