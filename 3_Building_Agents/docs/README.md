# 📚 Documentação — Module 3: Building Agents

Guias de estudo, cheat sheets e referências técnicas para construir agentes inteligentes.

## 📑 Índice

1. **[Estendendo Agentes com Ferramentas](01-extending-agents-with-tools.md)**
   - Conceito fundamental: LLMs raciocinam, mas precisam de ferramentas para agir
   - Tipos de ferramentas (APIs, funções, bancos de dados, execução de código)
   - Function Calling: a solução confiável para integração de tools
   - Implementação prática com schemas JSON
   - Armadilhas comuns e debugging

2. **[Structured Outputs: Tornando Respostas de IA Acionáveis](02-structured-outputs.md)**
   - Saídas estruturadas (JSON tipado) para integração com sistemas
   - Output parsers e function calling
   - Exemplo com Pydantic e estratégias de fallback

3. **[Gerenciamento de Estado em Agentes](03-agent-state-management.md)**
   - LLMs são apátridas: por que agentes precisam de estado
   - Estado efêmero como memória de trabalho da tarefa
   - State machines: passos modulares com TypedDict
   - Loop de execução e transições condicionais

4. **[Short-Term Memory em Agentes](04-short-term-memory.md)**
   - Memória como contexto simulado injetado no prompt
   - Taxonomia: estado (run) vs. sessão vs. longo prazo
   - Estratégias: histórico completo, janela deslizante e sumarização
   - Diferença entre estado do agente e memória de sessão

5. **[Ferramentas Externas e APIs](05-external-apis-and-tools.md)**
   - APIs como ponte entre raciocínio e ação no mundo real
   - Autenticação: API Key vs OAuth
   - Tratamento de falhas: retry, fallback e escalação
   - Observabilidade, segurança e mínimo de privilégio
   - Model Context Protocol (MCP): o padrão emergente para tool use

6. **[Agentes de Busca na Web](06-web-search-agents.md)**
   - Web search vs. web browsing: diferenças e escopo
   - Grounding: ancorar respostas em evidências verificáveis
   - APIs de busca: SerpAPI, Tavily e Bing
   - Pipeline de interpretação e seleção de resultados
   - Armadilhas: ruído, desinformação e dados desatualizados

7. **[Interagindo com Bancos de Dados](07-interacting-with-databases.md)**
   - Agentes que lêem e escrevem em dados estruturados reais
   - Tipos de BD: relacional, NoSQL, vetorial e grafo
   - text2SQL: tradução de linguagem natural para SQL com guardrails
   - Busca semântica com bancos vetoriais e cosine similarity
   - RAG como padrão arquitetural (não depende de vetores)
   - Abordagem híbrida: SQL filtra, vetor ranqueia
