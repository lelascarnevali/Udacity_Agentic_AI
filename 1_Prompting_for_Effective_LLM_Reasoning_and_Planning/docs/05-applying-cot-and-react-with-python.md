````markdown
# Aplicando Prompting CoT e ReAct com Python

> **Nota Técnica**: Este guia foca na **implementação de código** (Code-First) dos conceitos de Chain-of-Thought e ReAct. Baseado no exercício prático de diagnóstico de supply chain/retail da aula.

---

## 1. O Padrão de Engenharia (The Engineering Pattern)

Para construir um agente ReAct funcional em Python, não basta um bom prompt. Precisamos de uma arquitetura de loop (Runtime Loop) que gerencie o estado da conversa e a execução de ferramentas.

### Arquitetura do Loop (The ReAct Cycle)

O framework opera em um ciclo contínuo de retroalimentação. Visualize o fluxo de dados:

```ascii
[ LLM (Brain) ]  ---> "ACT: tool(arg)" ---> [ Parser (Code) ]
      ^                                            |
      |                                            v
[ History ] <--- "OBSERVATION: result" <--- [ Tool Execution ]
```

1.  **System Prompt**: Define as regras do jogo (THINK/ACT).
2.  **User Task**: O gatilho inicial.
3.  **Iteration Loop**: O script Python orquestra a troca de mensagens até que o LLM decida parar (`final_answer`).

---

## 2. Construindo o System Prompt (The Blueprint)

O prompt do sistema é o "sistema operacional" do agente. Ele deve conter 4 componentes críticos:

| Componente | Função | Exemplo (Logistics Agent) |
| :--- | :--- | :--- |
| **Role** | Identidade | *"You are a Supply Chain Logistics Coordinator."* |
| **Instruction** | Regra de Sintaxe | *"Respond with a single THINK/ACT message."* |
| **Tools** | API Doc | *"get_shipment_status(id): Get location..."* |
| **Few-Shot** | Exemplo Completo | *"User: Help! -> Assistant: THINK... ACT..."* |

### Code Snippet: Definição de Ferramentas
```python
tools_description = """
Available Tools:
1. get_shipment_status(tracking_id: str)
   - Use this to get the last known location.
   - Example: ACT: get_shipment_status(tracking_id="XYZ123")

2. check_facility_alerts(facility_name: str)
   - Use this to check for weather/operational alerts.

3. final_answer(summary: str)
   - Use ONLY when diagnosis is complete.
"""
```

---

## 3. O Ciclo de Execução (The Turn-by-Turn)

Visualização de como o agente "pensa" e "age" sequencialmente para resolver um problema complexo.

### Caso de Uso: Diagnóstico de Entregas (Logística) ou Vendas (Varejo)

#### Turno 1: Investigação Inicial
*   **User**: "Why is shipment XYZ123 delayed?"
*   **Agent (THINK)**: "I need status and location first."
*   **Agent (ACT)**: `get_shipment_status("XYZ123")`
*   **System (OBSERVE)**: `{"status": "Delayed", "location": "Chicago Rail Yard"}`

#### Turno 2: Correlação de Dados
*   **Agent (THINK)**: "It's in Chicago. I should check for alerts there."
*   **Agent (ACT)**: `check_facility_alerts("Chicago Rail Yard")`
*   **System (OBSERVE)**: `{"alert": "Severe Weather: Operations Suspended"}`

#### Turno 3: Conclusão
*   **Agent (THINK)**: "I have the root cause (Weather)."
*   **Agent (ACT)**: `final_answer("Delayed in Chicago due to severe weather.")`

---

## 4. O "Porquê" Funciona (Cognitive Architecture)

Por que o ReReact é superior ao Chain-of-Thought (CoT) isolado em tarefas dinâmicas?

| Característica | **Chain-of-Thought (CoT)** | **ReAct (CoT + Tools)** |
| :--- | :--- | :--- |
| **Metáfora** | O Estudioso na Biblioteca. | O Detetive em Campo. |
| **Acesso a Dados** | Limitado ao Treino (Cutoff Knowledge). | Ilimitado (Web, APIs, DBs). |
| **Decisão** | Linear ("Vou daqui até lá"). | Iterativa ("Tento X, se falhar, tento Y"). |
| **Correção de Erro** | Difícil (Alucinação em cascata). | Fácil (Observa erro da API e tenta de novo). |

> **Use Case**: Se você precisa de *Conhecimento Estático* (ex: Resumir um texto), use CoT. Se precisa de *Conhecimento Dinâmico* (ex: Preço atual do Bitcoin), use ReAct.

---

## 5. Implementação Prática (Regex Parsing)

O desafio real de engenharia é traduzir o texto livre do LLM ("I will use tool X") em uma chamada de função Python. O uso de **Expressões Regulares (Regex)** é o padrão da indústria para isso.

### Code Pattern: O Parser Robusto
O código abaixo demonstra como extrair o nome da ferramenta e seus argumentos de forma segura.

```python
import re

def parse_llm_response(response_text):
    # Procura pelo padrão: ACT: tool_name(arguments)
    match = re.search(r"ACT: (\w+)\((.*)\)", response_text)
    
    if match:
        tool_name = match.group(1)
        tool_args = match.group(2)
        return tool_name, tool_args
    return None, None

# Simulando o Loop
history = []
while True:
    response = llm.generate(history) # Ex: "ACT: get_weather(day='today')"
    tool, args = parse_llm_response(response)
    
    if tool:
        result = execute_tool(tool, args) # Retorna "Sunny"
        formatted_obs = f"OBSERVATION: {result}"
        history.append(formatted_obs)
    
    if tool == "final_answer":
        break
```

### Dica de Debugging
Se o seu agente ficar "preso" alucinando ferramentas inexistentes, adicione um `OBSERVATION: Tool not found` quando o parser falhar. Isso ensina o modelo a tentar de novo.

---

**Contexto utilizado:**
- **Skills:** `create-study-guide` (Code-First Approach).
- **Source 1:** Transcrições (`Applying...Subtitles`) com foco na implementação do Loop ReAct e Parsing.
- **Source 2:** Exemplos do Usuário (Supply Chain, Patient Diagnosis) para ilustrar a diferença dinâmica CoT vs ReAct.
- **Conceitos:** Runtime Loop, Tool Definition, Dynamic Information Retrieval.

````

---

**Tópico anterior:** [Chain-of-Thought & ReAct](04-chain-of-thought-and-react-prompting.md)
**Próximo tópico:** [Refinamento de Instruções de Prompt e Aplicação](06-prompt-instruction-refinement-and-application.md)
