# Encadeamento de Prompts com Python

## 1. Conceito Fundamental

**Prompt Chaining** é a técnica de quebrar tarefas complexas em etapas sequenciais, onde a saída de um prompt alimenta o próximo. Isso aumenta a confiabilidade e a clareza dos resultados.

$$
	ext{Prompt Chaining} = (\text{Prompt}_1 \xrightarrow{LLM} \text{Output}_1) \rightarrow (\text{Prompt}_2(\text{Output}_1) \xrightarrow{LLM} \text{Output}_2) \rightarrow \cdots
$$

---

## 2. Componentes da Arquitetura

- **LLM**: Modelo de linguagem que executa cada etapa
- **Prompt**: Instrução textual para o LLM
- **Chaining**: Encadeamento de prompts e respostas
- **Gate Check**: Validação automática (ex: sintaxe, schema)
- **Pydantic**: Estruturação e validação de dados

---

## 3. Comparativo: Chaining Tradicional vs Validado

|                     | Chaining Tradicional | Chaining Validado (Recomendado) |
|---------------------|---------------------|-------------------------------|
| Validação de saída  | ❌ Não               | ✅ Sim (AST/Pydantic)          |
| Robustez            | Média               | Alta                          |
| Debugging           | Manual              | Automatizado                  |
| Padronização        | Baixa               | Alta                          |
| Uso em produção     | Arriscado           | Seguro                        |

> **Dica:** Sempre prefira o chaining validado para aplicações reais!

---

## 4. Exemplo Prático: Data Analysis Script Generation

- **Objetivo:** Criar um script Python que leia um CSV (`input_data.csv`), calcule a média da coluna `value` e grave o resultado em `output.txt`.
- **Estratégia:** Dividir o problema em etapas, usar a saída de um prompt como entrada do próximo, e validar entre etapas com gate checks.

---

## 1. Implementando o encadeamento (prompt chaining)

O encadeamento é basicamente sobre construir e manipular strings e fazer chamadas sequenciais para a API do LLM. A seguir está um exemplo minimalista de como organizar as etapas.

### Passo 1 — Gerar o outline

Exemplo de prompt (padrão):

```python
# Prompt inicial para gerar um esboço
prompt_step1 = """
You are a helpful programming assistant.

I need a Python script to read a CSV file named 'input_data.csv',
calculate the average of a column named 'value', and write the
average to a new file named 'output.txt'.

Please provide a simple, step-by-step outline for this script.
"""

outline_response = get_completion(prompt_step1)
print(outline_response)
```

Exemplo de saída esperada (resumida):

1. Importar `csv`.
2. Abrir e ler `input_data.csv`.
3. Extrair a coluna `value` e converter para number.
4. Calcular a média.
5. Escrever o resultado em `output.txt`.

### Passo 2 — Gerar o código a partir do outline

O próximo prompt reutiliza o texto retornado pelo primeiro passo.

```python
prompt_step2 = f"""
You are a helpful programming assistant.

Based on the following outline, please write the complete Python code for the script.
Ensure you use standard libraries and include comments.

Outline:
---
{outline_response}
---
"""

code_response = get_completion(prompt_step2)
print(code_response)
```

Exemplo de código gerado (simplificado):

```python
import csv

def analyze_data():
    values = []
    try:
        with open('input_data.csv', 'r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                values.append(float(row['value']))
    except FileNotFoundError:
        print("Error: input_data.csv not found.")
        return

    average = sum(values) / len(values) if values else 0

    with open('output.txt', 'w') as outfile:
        outfile.write(f"The average is: {average}")

if __name__ == '__main__':
    analyze_data()
```


## 2. 🛡️ Gate Check — Validação Automática

Antes de executar código gerado dinamicamente, use uma verificação de sintaxe. O módulo `ast` permite checar se o código contém erros de sintaxe sem executá-lo.

```python
import ast

def check_python_syntax(code: str):
    try:
        ast.parse(code)
        return True, "No syntax errors found."
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"

# Uso:
# is_valid, message = check_python_syntax(code_response)
```

> **Debugging:**
> Se a checagem falhar, reencaminhe o código e a mensagem de erro ao modelo pedindo correção e repita o gate check. Exemplo de prompt para autocorreção:
>
> "Corrija o seguinte código Python para remover o erro de sintaxe abaixo.\nErro: {mensagem_de_erro}\nCódigo:\n{codigo}" 

> **Cenário real:**
> Se o LLM gerar código inválido, automatize o feedback e a revalidação até passar no gate check.


## 3. 🧰 Pydantic — Estruturar e Validar Saídas

Para garantir outputs consistentes das respostas do LLM (por exemplo, quando pedimos JSON), use `pydantic` para declarar e validar o formato esperado.

**Vantagens:**
- ✅ Validação automática de tipos e presença de campos
- ✅ Parsing para objetos Python com acesso por atributos
- ✅ Mensagens de erro claras para usar em gate checks

> **Fórmula:**
> $$\text{Validação} = \text{Pydantic}(\text{output\_json}) \xrightarrow{parse/validate} \text{objeto\_Python}$$

### Exemplo: modelos `OrderItem` e `Order` 🛒

### Exemplo: modelos `OrderItem` e `Order`

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class OrderItem(BaseModel):
    sku: str = Field(..., description="Stock Keeping Unit")
    quantity: int = Field(..., description="Quantidade do item")
    item_name: Optional[str] = Field(None, description="Nome do item, se disponível")


class Order(BaseModel):
    order_id: int = Field(..., description="Identificador único do pedido")
    customer_email: Optional[str] = Field(None, description="Email do cliente")
    items: List[OrderItem] = Field(..., description="Lista de itens do pedido")
    total_amount: float = Field(..., description="Valor total do pedido")
```

Como usar em um gate check:

```python
from pydantic import ValidationError

def validate_order(json_data: dict):
    try:
        order = Order.parse_obj(json_data)
        return True, order
    except ValidationError as e:
        return False, e.json()
```

### Como incluir o modelo no prompt

Ao solicitar que o modelo gere JSON, inclua a descrição dos campos (ou um esquema JSON) no prompt. Exemplo curto:

"""
Return a JSON object matching the following schema:
{
  "order_id": int,
  "customer_email": optional str,
  "items": [{"sku": str, "quantity": int, "item_name": optional str}],
  "total_amount": float
}
Respond only with valid JSON.
"""

Em seguida, parse a resposta do modelo e valide com Pydantic antes de prosseguir na cadeia.

## 4. Boas práticas e recomendações

- Sempre dividir tarefas complexas em etapas e validar entre etapas (gate checks).
- Peça ao LLM para responder em um formato estrito (JSON) quando o dado for consumido por código.
- Use `ast` para checagem rápida de sintaxe e `pydantic` para validação de conteúdo/estrutura.
- Mantenha prompts curtos e com instruções claras sobre o formato de saída.

## 5. Exemplo rápido de fluxo completo (pseudo-code)

```python
# 1. Gerar outline
outline = get_completion(prompt_outline)

# 2. Gerar código com base no outline
code = get_completion(prompt_code.format(outline=outline))

# 3. Gate check de sintaxe
ok, msg = check_python_syntax(code)
if not ok:
    # pedir correção ao modelo, repetir
    code = get_completion(prompt_fix.format(code=code, error=msg))

# 4. (Opcional) validar saídas estruturadas com pydantic
# 5. Executar com segurança (em sandbox) ou revisar manualmente
```

---

**Contexto utilizado:**
- Arquivos criados/alterados: [1_Prompting_for_Effective_LLM_Reasoning_and_Planning/docs/9-chaining-prompts-with-python.md](1_Prompting_for_Effective_LLM_Reasoning_and_Planning/docs/9-chaining-prompts-with-python.md)
- Skills consultadas: nenhuma
- Memória consultada: nenhuma
