---
agent: 'agent'
description: 'Cria um commit git com mensagem convencional analisando o diff atual. Detecta tipo, escopo e descrição automaticamente.'
tools: ['codebase', 'runCommands', 'editFiles']
---

Siga o skill `git-commit` localizado em `.github/skills/git-commit/SKILL.md` para criar um commit git convencional.

**Passos obrigatórios:**

1. Leia `.github/skills/git-commit/SKILL.md` para o workflow completo.
2. Consulte `.github/agents/memory/terminal-troubleshooting.md` para evitar erros conhecidos.
3. Execute `git status` e `git diff --staged` (ou `git diff`) para analisar as mudanças.
4. Detecte automaticamente: tipo (`feat`, `fix`, `docs`, `chore`, …), escopo e descrição.
5. Apresente a mensagem gerada para confirmação antes de executar o commit.
6. Execute o commit somente após aprovação.

**Argumento opcional:** Se o usuário forneceu um tipo ou escopo específico (ex: `docs(exercises)`), use-o como ponto de partida.
