# Aplicando Refinamento de Instruções de Prompt com Python

Este guia explora como transformar *prompts vagos* em *instruções precisas e programáveis*, utilizando Python para estruturar a interação com o LLM. A técnica é demonstrada através de dois cenários: um de **classificação de receitas** (baseado na aula) e um de **automação de suporte ao cliente** (aplicação prática).

## 1. O Ciclo de Refinamento (The Refinement Cycle)

O refinamento de prompts não é linear; é um ciclo iterativo de execução, análise e melhoria crítica.

```ascii
   +-------------+       +-------------+       +-------------+
   |   Initial   |       |   Analyze   |       |   Refined   |
   |   Prompt    | ----> |   Outputs   | ----> |   Prompt    |
   +------+------+       +------+------+       +------+------+
          ^                     |                     |
          |                     v                     |
          +-------------- <Evaluation> <--------------+
                         (Repeat Loop)
```

## 2. Cenário Teórico: Classificação de Receitas

Na aula, analisamos um prompt para verificar restrições dietéticas (ex: "Isso é vegano?"). A evolução demonstra a importância de especificar o **formato de saída** e **critérios de decisão**.

### Comparativo: Draft Inicial vs. Prompt Final

| Componente | Prompt Inicial (Vago) | Prompt Final (Refinado) |
| :--- | :--- | :--- |
| **Role (Papel)** | Não especificado | "Consultor Dietético Especialista" |
| **Task (Tarefa)** | "Analise a receita e diga se satisfaz as restrições" | "Analise ingredientes críticos, explique o raciocínio e classifique com certeza" |
| **Output** | Texto livre ou JSON simples | **JSON Estruturado** com chaves: `classification`, `explanation`, `critical_ingredients` |
| **Ambiguidade** | Inconsistente (ex: óleo "geral") | Regras explícitas (ex: "Óleo vegetal é plant-based a menos que notado") |
| **Opções** | Satisfied / Not Satisfied | Satisfied / Not Satisfied / **Undeterminable** |

---

## 3. Aplicação Prática: Automação de Suporte (Code-First)

Neste exercício, vamos aplicar o refinamento para criar uma ferramenta de triagem de emails de suporte.

### O Desafio: "From Vague Ideas to Precise Instructions"

**Objetivo:** Classificar emails de clientes, extrair o ID do usuário e determinar a urgência.

#### ❌ Abordagem Vaga (Don't Do This)

```python
prompt = """
Leia este email de suporte. Diga-me sobre o que é, se ele parece zangado
e qual é o ID do cliente se houver um.
"""
# Problemas:
# 1. "Sobre o que é" gera resumos inconsistentes.
# 2. "Parece zangado" é subjetivo.
# 3. Formato de saída não estruturado (difícil de parsear via código).
```

#### ✅ Abordagem Refinada (Structured JSON)

Este padrão força o LLM a raciocinar passo-a-passo e entregar dados prontos para API.

```python
import openai
import json

# Configuração do Cliente
client = openai.OpenAI()

email_content = """
Subject: ACESSO BLOQUEADO - URGENTE!!!
De: cliente_12345@email.com

Olá, estou tentando acessar minha conta (ID: 998877) há 2 horas e recebo erro 503.
Preciso fechar a folha de pagamento hoje!!! Resolvam isso agora.
"""

# Prompt Refinado com Estrutura JSON
system_instruction = """
ROLE:
Você é um Agente Sênior de Triagem de Suporte Técnico.

TASK:
Analise o email recebido e extraia informações estruturadas para o sistema de tickets.

RULES:
1. Urgency: Classifique como 'High' se houver bloqueio financeiro ou prazos explícitos.
2. Summary: Resuma o problema em no máximo 10 palavras.
3. Customer_ID: Extraia apenas números. Se não houver, retorne null.
4. Category: Escolha entre [Login, Billing, Technical, Feature Request].

OUTPUT FORMAT:
Retorne APENAS um objeto JSON com as seguintes chaves:
{
  "Category": "string",
  "Summary": "string",
  "Urgency": "Low" | "Medium" | "High",
  "Customer_ID": "string | null",
  "Reasoning": "string (explicação breve da urgência)"
}
"""

def analyse_support_email(email_text):
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Recomenda-se modelos capazes de JSON Mode
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": email_text}
        ],
        response_format={"type": "json_object"}, # Força saída JSON válida
        temperature=0.0
    )
    
    return response.choices[0].message.content

# Execução
raw_json = analyse_support_email(email_content)
ticket_data = json.loads(raw_json)

# Exibição do Resultado Processado
print(f"Ticket Criado: [{ticket_data['Category']}] - {ticket_data['Customer_ID']}")
print(f"Prioridade: {ticket_data['Urgency'].upper()}")
print(f"Motivo: {ticket_data['Reasoning']}")
```

### Output Esperado

O código acima garante que, independentemente da verborragia do cliente, o sistema receba dados limpos:

```json
{
  "Category": "Technical",
  "Summary": "Erro 503 impedindo fechamento folha pagamento",
  "Urgency": "High",
  "Customer_ID": "998877",
  "Reasoning": "Cliente cita bloqueio de folha de pagamento e erro de acesso persistente."
}
```

## 4. Padrões de Robustez (Robustness Patterns)

Ao trabalhar com instruções refinadas, considere sempre tratar falhas de parsing.

### JSON Parsing Seguro

Mesmo com `json_object`, é prudente validar as chaves essenciais:

```python
def validate_ticket(data):
    required_keys = ["Category", "Urgency", "Customer_ID"]
    missing = [key for key in required_keys if key not in data]
    
    if missing:
        raise ValueError(f"LLM falhou em gerar chaves obrigatórias: {missing}")
    
    # Normalização de ID
    if data["Customer_ID"]:
        data["Customer_ID"] = str(data["Customer_ID"]).strip()
        
    return data
```

## 5. Resumo das Melhores Práticas

1.  **Dê ao Modelo uma "Persona"**: `ROLE` define o tom e a competência esperada.
2.  **Use Delimitadores**: Separe instruções, contexto e dados de entrada.
3.  **Especifique o Esquema (Schema)**: Mostre *exatamente* o JSON que você quer (chaves e tipos).
4.  **Peça Raciocínio Antes da Decisão**: Adicionar um campo `Reasoning` ou `Explanation` no JSON melhora a precisão da classificação final (`Urgency`), pois força o modelo a "pensar" antes de rotular.
