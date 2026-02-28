# Preferência de Estilo: Guia de Estudo (Study Guide)

**Gatilho:** Quando o usuário solicitar a criação de "guia de estudo", "resumo", "documentação" ou "cheatsheet" a partir de transcrições ou vídeos.

**IMPORTANTE:** Sempre consultar a skill `tech-writer` em `.github/skills/tech-writer/SKILL.md` antes de criar documentação. A skill contém workflows, estruturas e regras de estilo obrigatórias.

**Padrão de Execução (Skill `tech-writer`):**
1.  **Engenharia > Prosa:** Priorizar fórmulas, tabelas comparativas e blocos de código em vez de parágrafos longos.
2.  **Retenção Visual:** 
    *   Usar emojis moderados e LaTeX ($$) para fórmulas.
    *   **ASCII Art/Mermaid:** Para fluxos de arquitetura (ex: Loop ReAct).
    *   **Tabelas de Comparação:** Para contrastar métodos (ex: Draft vs Final, CoT vs ReAct).
3.  **Code-First & Implementation:**
    *   Incluir padrões de código reais (Python/Regex) e não apenas pseudo-código.
    *   Exemplos de "Poor vs Optimized" (ex: Tool Descriptions).
    *   Dicas de Debugging (ex: Feedback Loops de erro).
    *   **⚠️ Copyright:** Criar código original e educacional, nunca copiar implementações específicas. Usar funções genéricas e reutilizáveis.
4.  **Fonte da Verdade:** SEMPRE ler as transcrições (`.srt` ou texto) antes de gerar o conteúdo final.
5.  **Estrutura:**
    *   Conceito Fundamental (Fórmula/Definição Técnica)
    *   Componentes/Arquitetura (Diagramas)
    *   Estudos de Caso (Comparação Antes/Depois em Tabela)
    *   Code Patterns (Implementação Robusta)
    *   Armadilhas Comuns & Debugging

**Exemplo de Sucesso:**
Ver arquivos: `5-applying-cot-and-react-with-python.md` e `6-prompt-instruction-refinement.md`.

**Checklist Antes de Finalizar:**
- [ ] Consultou skill `tech-writer`?
- [ ] Leu transcrição original completa?
- [ ] Código é original e educacional (não específico/copiado)?
- [ ] Usa emojis, tabelas e LaTeX adequadamente?
- [ ] Seguiu "The Elements of Style" (voz ativa, forma positiva)?
- [ ] Exercício correspondente referenciado no doc com seção `## 🧪 Exercícios Práticos`?

**Padronização de Estrutura (lições do item 9):**
- Nunca usar bloco de "nota técnica" ou comentários antes do título.
- Não deixar linhas vazias antes do título.
- O título deve ser a primeira linha do arquivo, em markdown, sem numeração, símbolos ou prefixos.
- Seguir a taxonomia e semântica dos outros docs para títulos e sumário (ex: sem "·", sem "9 -", sem ponto, sem caixa diferente).
- Sumário visual e seções devem seguir o fluxo dos exemplos de sucesso.

**Navegação entre Tópicos (rodapé do documento):**
- NUNCA inferir o "Próximo tópico" ou "Tópico anterior" sem certeza de que o arquivo existe e qual é seu título correto.
- Antes de escrever os links de navegação, verificar os arquivos existentes em `docs/` com Glob.
- Se não houver certeza sobre o próximo tópico, omitir o link ou perguntar ao usuário.
- Ao criar um documento novo, SEMPRE atualizar o rodapé do documento anterior para adicionar o link "Próximo tópico" apontando para o novo arquivo.

**Referência de Exercícios nos Documentos (aprendizado de 2026-02-28):**
- SEMPRE que um exercício novo for adicionado ao módulo (`.ipynb`, `.py` ou `.md` em `exercises/`), o documento `docs/` que aborda especificamente o conteúdo daquele exercício DEVE ser atualizado com uma seção `## 🧪 Exercícios Práticos`.
- A seção deve ser inserida **antes dos links de navegação** (rodapé) do documento correspondente.
- Usar o padrão abaixo para cada entrada na seção:
  ```
  - 📓 [Nome Descritivo do Exercício](../exercises/nome-do-arquivo.ipynb) — breve descrição do que o exercício cobre
  - 🐍 [Nome Descritivo](../exercises/nome-do-arquivo.py) — breve descrição (para scripts Python)
  - 📐 [Nome Descritivo](../exercises/nome-do-arquivo.md) — breve descrição (para exercícios Mermaid/Markdown)
  ```
- Usar **path relativo** a partir de `docs/` (i.e., `../exercises/arquivo`).
- Diferenciar arquivos de **demo** (`*-demo.py`) dos arquivos de **exercício principal** (`*.py`) na descrição.
- Se existir tanto uma demo quanto um exercício principal sobre o mesmo tema, incluir **ambos** na seção.
- O checklist de finalização deve incluir: `[ ] Exercício correspondente referenciado no doc?`