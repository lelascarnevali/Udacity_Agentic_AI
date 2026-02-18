# Guia de Referência: Chaining Prompts para Raciocínio Agêntico

## 1. Conceito Fundamental: Por que Encadear Prompts?

**Limitações dos LLMs em Tarefas Complexas:**
- LLMs tradicionais são otimizados para operações simples de entrada-saída única
- Operações multi-etapa com dependências podem causar confusão e erros
- Tarefas que requerem dados externos (não presentes no treinamento) necessitam abordagens especiais

**Solução: Prompt Chaining**
Quebrar tarefas complexas em sub-tarefas menores e gerenciáveis, cada uma com seu próprio prompt, conectadas programaticamente.

### Analogia
Pedir a um não-padeiro para "assar um bolo de múltiplas camadas" → Falha provável  
Dar instruções passo-a-passo → Sucesso mais provável

---

## 2. Sequential Prompting (Prompting Sequencial)

**Definição:** Raciocínio multi-etapa que quebra uma tarefa complexa em uma série de sub-tarefas sequenciais.

### Exemplo: LinkedIn Post sobre AI Agents

**❌ Abordagem Única (Problema):**
```
"Pesquise agentes de IA, resuma os conceitos-chave e escreva um post no LinkedIn sobre eles."
```

**✅ Abordagem Sequencial (Solução):**
```
Prompt 1: "Pesquise conceitos-chave de agentes de IA."
         → RESPONSE_1

Prompt 2: "Resuma a seguinte informação: {RESPONSE_1}"
         → RESPONSE_2

Prompt 3: "Escreva um post no LinkedIn baseado neste resumo: {RESPONSE_2}"
         → FINAL_RESPONSE
```

### Benefícios
- ✅ Espelha resolução de problemas humana
- ✅ Permite iteração e melhoria individual de cada prompt
- ✅ Melhora precisão ao focar em uma meta por vez
- ✅ Facilita debugging e manutenção

---

## 3. Prompt Chaining (Encadeamento de Prompts)

**Definição:** Conexão programática de prompts onde a saída de uma chamada LLM se torna entrada da próxima.

### Estrutura Básica
```python
# Chamada 1: Pesquisa
RESPONSE_1 = call_llm("Pesquise conceitos-chave de agentes de IA.")

# Chamada 2: Resumo
prompt_2 = f"Resuma os seguintes conceitos: {RESPONSE_1}"
RESPONSE_2 = call_llm(prompt_2)

# Chamada 3: Draft
prompt_3 = f"Escreva um post no LinkedIn baseado neste resumo: {RESPONSE_2}"
FINAL_RESPONSE = call_llm(prompt_3)
```

### Exemplo Prático: Consulta de Calendário

**Workflow Hard-coded:**
1. LLM determina se precisa de dados do calendário
   - Input: "Esta consulta requer dados do calendário? QUERY: Que horas é meu dentista amanhã?"
   - Output: "Sim"
2. Se "Sim", orquestrador chama `get_calendar()`
3. LLM usa dados do calendário para responder
   - Input: `{calendar_data}`
   - Output: "Seu dentista é às 9h."

**Workflow Agêntico (ReAct Framework):**
```
User: "Que horas é meu dentista amanhã?"

LLM: THOUGHT: Preciso chamar get_calendar.
     ACTION: get_calendar("tomorrow")

Orchestrator: Executa get_calendar() → {"9am"}

LLM: OBSERVATION: {"9am"}
     THOUGHT: É às 9am. Retornar resposta final.
     ACTION: final_answer("9am")
```

---

## 4. Output Validation: Gate Checks

**Problema:** LLMs podem alucinar, produzir formatos incorretos ou falhar em seguir instruções. Um erro em uma etapa inicial pode comprometer todo o processo (efeito dominó).

**Solução:** Gate Checks são validações programáticas colocadas entre etapas de uma cadeia.

### Fluxo de Decisão
```
output = call_llm(prompt_step1)
    ↓
Gate Check: Validação
    ↓
✅ PASS → Continue para próxima etapa
❌ FAIL → Erro/Retry/Retry com feedback
```

### Tipos de Gate Checks

#### 1. **Format Checks (Verificação de Formato)**
- Estrutura (JSON, XML)
- Comprimento
- Campos obrigatórios
- **Ferramentas:** Pydantic, structured outputs

#### 2. **Content Checks (Verificação de Conteúdo)**
- Keywords e frases específicas
- Tópicos e relevância
- **Ferramentas:** Regex, embeddings semânticos, outros LLMs

#### 3. **Logic Checks (Verificação de Lógica)**
- Sentido numérico/lógico
- Para código: compila? Importa bibliotecas restritas? Valores numéricos razoáveis?
- **Ferramentas:** AST parsing, linters, execução sandbox

### Pseudo-código
```python
output = call_llm(prompt_step1)

if validate_output(output):
    next_input = process(output)
    call_llm(prompt_step2, next_input)
else:
    handle_error(output)
    # Opções: raise error, retry, retry com feedback
```

### Estratégias de Falha
1. **Halt:** Parar execução e reportar erro
2. **Retry:** Tentar novamente com mesmo prompt
3. **Feedback Loop:** Tentar novamente incluindo motivo da falha no prompt

---

## 5. Caso de Uso: Geração de Script de Análise de Dados

**Tarefa:** Criar script Python para ler CSV, calcular média de coluna e escrever resultados em novo CSV.

### Cadeia Completa

#### **Step 1: Gerar Outline**
```
Prompt: "Você é um assistente de programação útil. Preciso de um script 
Python para ler um CSV, calcular a média de uma coluna e escrever os 
resultados em um novo CSV. Forneça um outline passo-a-passo simples."

Expected Output: Lista numerada ou com bullets de passos de alto nível

Gate Check 1 (Opcional): Verificação programática de formato de lista
                        e frases-chave como "read", "process", "write"
```

#### **Step 2: Gerar Código**
```
Prompt: "Baseado no seguinte outline, escreva o código Python. 
Use bibliotecas padrão como 'csv' e 'statistics'.
Outline: [Inserir Output do Step 1]"

Expected Output: Código Python

Gate Check 2: Validar sintaxe do código
              Implementação: ast.parse() ou linters (flake8, pylint)
              Resultado: Se falhar, parar ou ir para refinamento
```

#### **Step 3: Refinar Código (Se Gate Check 2 Falhou)**
```
Prompt: "O seguinte código Python contém erros de sintaxe:
[Inserir Código do Step 2]
Feedback de erro: [Inserir Mensagens do Gate Check 2]
Corrija o código baseado neste feedback."

Expected Output: Código Python corrigido

Retry Gate Check 2: Se passar, prosseguir
                   Se falhar, desistir ou loop (máx. iterações)
```

### Diagrama de Fluxo
```
Prompt 1: Create Outline
    ↓
Gate Check 1 (Formatting)
    ↓
Prompt 2: Write Code
    ↓
Gate Check 2 (Check syntax)
    ↓
❌ FAIL → Prompt 3: Refinement → Gate Check 2
✅ PASS → Completed!
```

### Implementação em Python
```python
import ast
from typing import Tuple, Callable

def validate_syntax(code: str) -> Tuple[bool, str]:
    """Valida sintaxe Python usando AST."""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, str(e)

def chain_with_validation(
    prompts: list[str],
    validators: list[Callable],
    llm_call: Callable,
    max_retries: int = 2
) -> str:
    """Executa cadeia de prompts com validação entre etapas."""
    result = None
    
    for i, (prompt, validator) in enumerate(zip(prompts, validators)):
        # Primeira chamada ou usar resultado anterior
        if result:
            prompt = prompt.format(previous_output=result)
        
        result = llm_call(prompt)
        
        # Validar output
        is_valid, error = validator(result)
        retry_count = 0
        
        while not is_valid and retry_count < max_retries:
            feedback_prompt = f"""Previous output had issues:
            {result}
            
            Error: {error}
            
            Please correct and try again."""
            
            result = llm_call(feedback_prompt)
            is_valid, error = validator(result)
            retry_count += 1
        
        if not is_valid:
            raise ValueError(f"Step {i+1} failed after {max_retries} retries")
    
    return result

# Exemplo de uso
def simple_validator(output: str) -> Tuple[bool, str]:
    """Validador simples de exemplo."""
    if len(output) > 10:
        return True, ""
    return False, "Output too short"
```

---

## 6. Melhores Práticas

### ✅ DO's
- **Decomponha tarefas complexas** em sub-tarefas focadas
- **Use prompts especializados** para cada etapa
- **Implemente gate checks** em pontos críticos
- **Forneça feedback** nas tentativas de retry
- **Limite iterações** para evitar loops infinitos
- **Log todas as etapas** para debugging e auditoria

### ❌ DON'Ts
- Não crie prompts únicos gigantes para tarefas multi-etapa
- Não assuma que outputs estão sempre corretos
- Não ignore erros de etapas anteriores
- Não encadeie sem validação em aplicações críticas
- Não esqueça de tratar casos de falha

---

## 7. Padrões Comuns de Cadeia

### Pattern 1: Linear Chain
```
Task → Subtask 1 → Subtask 2 → Subtask 3 → Result
```

### Pattern 2: Conditional Chain
```
Task → Decision Point → Branch A / Branch B → Result
```

### Pattern 3: Iterative Refinement
```
Task → Generate → Validate → [If fail: Refine → Validate] → Result
```

### Pattern 4: Parallel Processing
```
Task → Subtask 1 \
       Subtask 2  → Merge → Result
       Subtask 3 /
```

---

## 8. Aplicações no Mundo Real

### Healthcare: Processamento de Registros Médicos
```
1. Extract patient data → Gate Check (PHI compliance)
2. Summarize findings → Gate Check (medical accuracy)
3. Generate report → Gate Check (format validation)
```

### Content Generation: Marketing Copy
```
1. Research topic → Gate Check (relevance)
2. Create outline → Gate Check (structure)
3. Write draft → Gate Check (brand guidelines)
4. Optimize SEO → Gate Check (keyword density)
```

### Code Generation & Debugging
```
1. Understand requirements → Gate Check (clarity)
2. Generate code → Gate Check (syntax)
3. Write tests → Gate Check (coverage)
4. Debug errors → Gate Check (all tests pass)
```

### Claims Triage (Seguros)
```
1. Extract claim data → Gate Check (required fields)
2. Classify urgency → Gate Check (policy rules)
3. Route to adjuster → Gate Check (assignment rules)
```

---

## 9. Comparação: Single Prompt vs. Prompt Chain

| Aspecto | Single Prompt | Prompt Chain |
|:---|:---|:---|
| **Complexidade** | Tarefas simples | Tarefas multi-etapa |
| **Controle** | Baixo | Alto (validação por etapa) |
| **Debugging** | Difícil | Fácil (isolar etapa com problema) |
| **Confiabilidade** | Variável | Alta (com gate checks) |
| **Manutenção** | Difícil modificar | Fácil (prompts modulares) |
| **Custo** | Baixo | Médio-Alto (múltiplas chamadas) |
| **Latência** | Baixa | Média-Alta (sequencial) |

---

## 10. Considerações de Implementação

### Gerenciamento de Estado
- Manter contexto entre etapas
- Persistir resultados intermediários
- Implementar rollback em caso de falha

### Performance
- Considerar custo de múltiplas chamadas LLM
- Otimizar prompts para reduzir tokens
- Implementar cache quando possível

### Escalabilidade
- Paralelizar etapas independentes
- Usar filas para processar cadeias longas
- Implementar rate limiting

### Monitoramento
- Log de cada etapa e gate check
- Métricas de sucesso/falha por etapa
- Alertas para falhas recorrentes

---

## 11. Ferramentas e Frameworks

### Bibliotecas Python
- **LangChain:** Framework completo para prompt chaining
- **Pydantic:** Validação de estruturas de dados
- **AST:** Parsing e validação de código Python
- **Flake8/Pylint:** Linters para code validation

### Padrões de Orquestração
- **Orchestration Layer:** Gerencia fluxo de execução
- **State Machine:** Controla transições entre etapas
- **Event-Driven:** Reage a outputs de etapas anteriores

---

## 12. Recap: Conceitos-Chave

✅ **Task Decomposition:** Problemas complexos devem ser quebrados em sub-tarefas focadas

✅ **Prompt Chaining:** Output de uma instrução AI torna-se input da próxima programaticamente

✅ **Output Validation:** Gate checks são críticos para confiabilidade e prevenir propagação de erros

✅ **Stage-Specific Prompting:** Usar prompts distintos e especializados para cada parte melhora precisão

✅ **Feedback Loops:** Incluir motivos de falha em retries melhora taxa de sucesso

---

## 13. Fórmulas e Equações

### Taxa de Sucesso da Cadeia
$$P_{chain} = \prod_{i=1}^{n} P_i$$

Onde $P_i$ é a probabilidade de sucesso da etapa $i$.

**Implicação:** Uma cadeia de 5 etapas com 90% de sucesso cada = $0.9^5 = 59\%$ de sucesso total.  
**Solução:** Gate checks aumentam $P_i$ individual.

### Custo de Retry com Feedback
$$C_{total} = C_{base} + \sum_{i=1}^{r} (C_{retry} + C_{validation})$$

Onde:
- $C_{base}$: custo da execução inicial
- $r$: número de retries
- $C_{retry}$: custo de cada retry
- $C_{validation}$: custo de cada gate check

---

## Recursos Adicionais

### Leitura Recomendada
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)

### Frameworks
- [LangChain Documentation](https://python.langchain.com/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/)

---

**Parabéns por dominar Chaining Prompts para Raciocínio Agêntico!** Esta é uma habilidade fundamental para construir agentes de IA confiáveis e capazes. Continue praticando a decomposição de tarefas, implementação de validações e iteração de prompts. 🚀
