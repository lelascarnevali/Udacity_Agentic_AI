# Preferência de Estilo: Guia de Estudo (Study Guide)

**Gatilho:** Quando o usuário solicitar a criação de "guia de estudo", "resumo", "documentação" ou "cheatsheet" a partir de transcrições ou vídeos.

**Padrão de Execução (Skill `create-study-guide`):**
1.  **Engenharia > Prosa:** Priorizar fórmulas, tabelas comparativas e blocos de código em vez de parágrafos longos.
2.  **Retenção Visual:** 
    *   Usar emojis moderados e LaTeX ($$) para fórmulas.
    *   **ASCII Art/Mermaid:** Para fluxos de arquitetura (ex: Loop ReAct).
    *   **Tabelas de Comparação:** Para contrastar métodos (ex: Draft vs Final, CoT vs ReAct).
3.  **Code-First & Implementation:**
    *   Incluir padrões de código reais (Python/Regex) e não apenas pseudo-código.
    *   Exemplos de "Poor vs Optimized" (ex: Tool Descriptions).
    *   Dicas de Debugging (ex: Feedback Loops de erro).
4.  **Fonte da Verdade:** SEMPRE ler as transcrições (`.srt` ou texto) antes de gerar o conteúdo final.
5.  **Estrutura:**
    *   Conceito Fundamental (Fórmula/Definição Técnica)
    *   Componentes/Arquitetura (Diagramas)
    *   Estudos de Caso (Comparação Antes/Depois em Tabela)
    *   Code Patterns (Implementação Robusta)
    *   Armadilhas Comuns & Debugging

**Exemplo de Sucesso:**
Ver arquivos: `5-applying-cot-and-react-with-python.md` e `6-prompt-instruction-refinement.md`.