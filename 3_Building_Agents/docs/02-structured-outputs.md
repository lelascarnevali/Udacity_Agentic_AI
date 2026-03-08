
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

Para esquemas complexos com listas e objetos aninhados, use Pydantic. O `MeetingSummary` contém uma lista de `ActionItem` — dois níveis de aninhamento. Pydantic valida o schema na construção: se o LLM retornar campos incorretos, um `ValidationError` é lançado imediatamente, permitindo retry ou fallback.

```python
from pydantic import BaseModel, Field
from typing import Annotated, List

class ActionItem(BaseModel):
    """Representa uma tarefa atribuída a um responsável."""
    task: Annotated[str, Field(description="Tarefa a ser executada")]
    assignee: Annotated[str, Field(description="Responsável pela tarefa")]
    due_date: Annotated[str, Field(description="Prazo de conclusão")]

class MeetingSummary(BaseModel):
    """Resumo estruturado de uma reunião."""
    title: Annotated[str, Field(description="Título da reunião")]
    date: Annotated[str, Field(description="Data da reunião")]
    participants: Annotated[List[str], Field(description="Participantes da reunião")]
    key_points: Annotated[List[str], Field(description="Pontos principais discutidos")]
    action_items: Annotated[List[ActionItem], Field(description="Tarefas geradas na reunião")]
```

## Diagrama: fluxo de saída estruturada

```mermaid
flowchart LR
  A[LLM (texto livre)] --> B[Output Parser / Function Caller]
  B -->|Valida| C[Typed JSON / Pydantic Model]
  B -->|Falha| D[Retry / Clarify / Fallback]
  C --> E[Downstream System (Tickets, DB, API)]
```

## As três estratégias de output parsing

| Estratégia | Parser | Quando usar |
|---|---|---|
| Texto livre | `StrOutputParser` | Respostas conversacionais simples |
| JSON genérico | `JsonOutputParser` | Estruturas conhecidas sem validação Pydantic |
| Modelo Pydantic | `PydanticOutputParser` | Contrato forte com validação de tipos e aninhamento |

## Implementação com `StructuredAgent`

A classe `StructuredAgent` encapsula o padrão de saída estruturada usando `response_format` e `JsonOutputParser`:

```python
from lib.llm import LLM
from lib.parsers import JsonOutputParser, PydanticOutputParser
from lib.messages import SystemMessage, UserMessage

class StructuredAgent:
    """Agente que retorna respostas em formato estruturado."""

    def __init__(self, role: str, instructions: str, output_model=None):
        self.role = role
        self.instructions = instructions
        self.output_model = output_model
        self.llm = LLM(model="gpt-4o-mini")

    def invoke(self, user_message: str) -> dict:
        messages = [
            SystemMessage(content=f"Role: {self.role}. {self.instructions}"),
            UserMessage(content=user_message),
        ]
        if self.output_model:
            # response_format instrui o modelo a produzir JSON compatível com o schema Pydantic
            ai_message = self.llm.invoke(input=messages, response_format=self.output_model)
            return JsonOutputParser().parse(ai_message)
        ai_message = self.llm.invoke(messages)
        return {"response": ai_message.content}
```

`response_format=output_model` instrui o LLM a produzir JSON compatível com o schema Pydantic. `JsonOutputParser().parse(ai_message)` decodifica o JSON de `ai_message.content` em um dicionário Python. Para validação rigorosa em tempo de execução, `PydanticOutputParser(model_class=MeetingSummary).parse(ai_message)` retorna uma instância tipada de `MeetingSummary`.

```python
# Exemplo de uso
agent = StructuredAgent(
    role="Meeting Assistant",
    instructions="Sumarize reuniões em formato estruturado.",
    output_model=MeetingSummary
)
summary = agent.invoke(meeting_transcript)

# Validação opcional com Pydantic
validated = MeetingSummary(**summary)
print(validated.action_items[0].assignee)
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

## 🧪 Exercícios Práticos

- 📓 [Structured Outputs — Demo](../exercises/2-structured-outputs-demo.ipynb) — demonstração completa do fluxo com `StructuredAgent`, `MeetingSummary` e `ActionItem`
- 📓 [Structured Outputs — Exercício](../exercises/2-structured-outputs-exercise.ipynb) — implemente `StructuredAgent` com `output_model`, `JsonOutputParser` e validação Pydantic

---

[← Tópico Anterior: Estendendo Agentes com Ferramentas](01-extending-agents-with-tools.md) | [Próximo Tópico: Gerenciamento de Estado em Agentes →](03-agent-state-management.md)
