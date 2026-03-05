
# Structured Outputs: Tornando Respostas de IA Acionáveis

> Agentes são muito mais úteis quando retornam saídas estruturadas e legíveis por máquina (JSON tipado) em vez de texto livre.

## Por que isso importa

Saídas estruturadas permitem que agentes integrem-se diretamente a sistemas downstream (ticketing, dashboards, alertas) sem parsing frágil. Ex.:

```json
{
  "issue_type": "login_problem",
  "urgency": "high",
  "customer_email": "jane@mail.com"
}
```

Texto livre é legível para humanos; JSON tipado é acionável por código.

## Por que prompting nem sempre basta

Pedir ao modelo para "retornar JSON" às vezes funciona, mas frequentemente produz campos inválidos ou ambíguos (ex.: `"urgency": "very"` ou `"customer_email": "none found"`). LLMs são ótimos com linguagem, não com regras estritas.

## Output parsers e Function Calling

Uma camada de *output parsing* valida se a resposta cumpre um esquema definido. Se falhar, a aplicação pode:

- Re-tentar com um prompt de clarificação
- Usar um fallback (ex.: pedir confirmação ao usuário)
- Logar o erro para debugging

Function calling (quando suportado pelo provedor) é ainda mais robusto: o modelo deve gerar um objeto de chamada de função que segue um JSON Schema, reduzindo respostas inválidas.

## Modelando dados complexos com Pydantic

Para esquemas complexos (listas, objetos aninhados, datas, enums) use Pydantic em Python. Exemplo de um `ActionItem`:

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class ActionItem(BaseModel):
    title: str
    due_date: datetime
    owner: str
    status: Literal["open", "closed"]

# Exemplo de uso: parsear a saída do modelo e validar
raw = get_model_output()
item = ActionItem.parse_raw(raw)
```

Pydantic fornece contrato e validação — se o modelo retornar `"status": "very"`, a validação falhará e a aplicação poderá agir.

## Diagrama: fluxo de saída estruturada

```mermaid
flowchart LR
  A[LLM (texto livre)] --> B[Output Parser / Function Caller]
  B -->|Valida| C[Typed JSON / Pydantic Model]
  B -->|Falha| D[Retry / Clarify / Fallback]
  C --> E[Downstream System (Tickets, DB, API)]
```

## Exemplo de Function Calling (esquema simplificado)

```json
{
  "name": "create_ticket",
  "arguments": {
    "type": "object",
    "properties": {
      "issue_type": {"type": "string"},
      "urgency": {"type": "string","enum":["low","medium","high"]},
      "customer_email": {"type":"string","format":"email"}
    },
    "required":["issue_type","urgency"]
  }
}
```

## Estratégias de resiliência

- Validar sempre com um parser antes de executar ações automatizadas.
- Em caso de falha, re-prompt com exemplos (few-shot) ou peça confirmação humana.
- Logar e monitorar falhas estruturais para melhorar prompts e schemas.

## Onde Pydantic se encaixa

Pydantic é a ponte entre o JSON gerado pelo LLM e os objetos tipados da aplicação: define esquemas, valida e converte tipos (e.g., `datetime`).

## Resumo rápido

- Use esquemas (JSON Schema / Pydantic) para contratos claros.
- Prefira function calling quando disponível.
- Valide sempre e projete estratégias de fallback.

---

[← Tópico Anterior: Estendendo Agentes com Ferramentas](01-extending-agents-with-tools.md) | [Próximo Tópico: Gerenciamento de Estado em Agentes →](03-agent-state-management.md)
