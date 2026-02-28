````markdown
# Chain-of-Thought & ReAct: Frameworks de Raciocínio

> **Nota Técnica**: Este guia aborda a transição de LLMs passivos (geradores de texto) para sistemas agênticos (resolutores de problemas). Foca em duas arquiteturas cognitivas essenciais: *Chain-of-Thought* (Raciocínio Interno) e *ReAct* (Raciocínio + Ação Externa).

---

## 1. O Problema da Complexidade (Why LLMs Fail?)

LLMs padrão operam estatisticamente prevendo o próximo token. Em tarefas complexas (lógica multi-etapa, acesso a dados em tempo real), essa abordagem falha por dois motivos:
1.  **Falta de Planejamento**: Tentativa de resolver o problema em um único passo ("One-shot generation").
2.  **Isolamento**: Incapacidade intuitiva de acessar ferramentas externas (calculadoras, APIs).

---

## 2. Chain-of-Thought (CoT): O "Show Your Work"

Técnica que força o modelo a gerar passos intermediários de raciocínio antes da resposta final. Transforma a "caixa preta" em uma "caixa branca" auditável.

### Variantes de CoT

| Tipo | Prompt Pattern | Exemplo |
| :--- | :--- | :--- |
| **Zero-Shot CoT** | Instrução Mágica | *"Let's think step by step."* (Simplesmente adicionar isso melhora lógica). |
| **Few-Shot CoT** | Exemplo Demonstrativo | *"Q: Roger tem 5 bolas... A: Roger começou com 5, ganhou 2..."* (Mostrar o raciocínio esperado). |

### Benefícios de Engenharia
*   **Performance:** Reduz alucinações em aritmética e lógica simbólica.
*   **Interpretabilidade:** Permite debugar onde a lógica falhou (no passo 2 ou 3?) antes do resultado final.

---

## 3. ReAct Framework: Reason + Act

Enquanto o CoT melhora o raciocínio interno, o **ReAct** conecta esse raciocínio ao mundo exterior. É o padrão fundamental para Agentes de IA.

### O Loop ReAct (The Loop)
O agente opera em um ciclo contínuo até satisfazer a requisição:

1.  **🧠 THOUGHT (Pensamento)**: O modelo planeja o próximo passo. *"Preciso saber a temperatura atual."*
2.  **🛠️ ACTION (Ação)**: O modelo solicita o uso de uma ferramenta. `get_weather("São Paulo")`
3.  **👀 OBSERVATION (Observação)**: O **Orquestrador** (código Python) executa a ferramenta e devolve o resultado. *"30 Graus, Ensolarado."*
    *   *Repete-se o ciclo com a nova informação.*

---

## 4. Implementação de Prompt ReAct

Abaixo, um padrão de prompt robusto para um **Financial Analyst Agent** (baseado no caso de uso fornecido).

```python
system_prompt = """
You are a diligent financial analyst assistant.
Use a step-by-step reasoning process. At each step, respond with ONE message:

THINK: Reason about the user's request and figure out the next logical step.
ACT: Call ONE of the available tools.

# Available Tools
1. get_stock_quote(ticker: str)
2. search_financial_news(company_name: str)
3. final_answer(summary: str) # Use ONLY when done.

# Example Consistency
User: "Compare P/E of MegaCorp ($MC) vs Innovate Inc ($II)."
Assistant:
THINK: I need P/E ratios for both. Starting with MegaCorp.
ACT: get_stock_quote(ticker="$MC")
"""
```

### Fluxo de Execução (Runtime)

1.  **User**: "Check weather in NYC."
2.  **LLM**: `THINK: I need weather data. ACT: get_weather('NYC')`
3.  **Orchestrator**: Executa API -> Retorna `OBSERVATION: 15°C, Rainy`.
4.  **LLM**: `THINK: I have the data. ACT: final_answer('It is 15°C and Rainy in NYC.')`

---

## 5. Comparativo de Arquiteturas

| Feature | Standard Prompting | Chain-of-Thought (CoT) | ReAct |
| :--- | :--- | :--- | :--- |
| **Foco** | Resposta Imediata | Raciocínio Lógico | Interação com Ambiente |
| **Estrutura** | Input -> Output | Input -> Steps -> Output | Input -> [Thought-Action-Obs] Loop -> Output |
| **Caso de Uso** | Email, Escrita Criativa | Problemas Matemáticos, Lógica | Agentes Autônomos, Web Search, Data Retrieval |
| **Complexidade** | Baixa | Média | Alta (Requer Orquestrador Externo) |

---
**Contexto utilizado:**
- **Skills:** `create-study-guide` (Tabelas, Emojis, Code Blocks).
- **Source 1:** User Text (Exemplos detalhados de Financial/Life Sciences Agent).
- **Source 2:** Transcrições (`Chain-of-Thought... Subtitles`) para definições canônicas de Zero-Shot/Few-Shot CoT e Loop ReAct.

````

---

## 🧪 Exercícios Práticos

Para aplicar os conceitos deste tópico na prática, consulte:

- 📓 [Lesson 2: Chain-of-Thought — Demand-Spike Detective, Parte I](../exercises/04-lesson-2-chain-of-thought-and-react-prompting-part-i.ipynb) — aplicação de prompts CoT para diagnosticar picos de vendas em dados de varejo
- 📓 [Lesson 2: ReAct — Demand-Spike Detective, Parte II](../exercises/05-lesson-2-chain-of-thought-and-react-prompting-part-ii.ipynb) — implementação do loop ReAct com tool calling e parsing de ações

---

**Tópico anterior:** [Implementando Role-Based Prompting](03-implementing-role-based-prompting.md)
**Próximo tópico:** [Aplicando CoT & ReAct com Python](05-applying-cot-and-react-with-python.md)
