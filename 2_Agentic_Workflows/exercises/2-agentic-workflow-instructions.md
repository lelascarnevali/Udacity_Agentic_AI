## Instruções para Modelagem Agentic com Mermaid

### Contexto
Você trabalhará com o primeiro fluxograma incompleto fornecido na descrição do exercício. O segundo fluxograma determinístico mais detalhado serve apenas para dar contexto sobre a lógica sequencial original que seu novo design agentic deve melhorar.

### Preparação do Workspace
- Abra o navegador e acesse [mermaid.live](https://mermaid.live) ou utilize seu editor Mermaid favorito.

### Passo 1: Diagrama Inicial
Copie o código Mermaid inicial abaixo para o editor:

```mermaid
flowchart TD
	Start[Start] --> Manage[Manage Aid Request]
	Manage --> Inventory[Check Inventory]
	Manage --> // Placeholder for other checks
	Inventory --> // Placeholder for result flow
	Manage --> DispatchDecision{Ready to Dispatch?}
	DispatchDecision -- Yes --> Dispatch[Dispatch Team]
	DispatchDecision -- No --> Replan[Replan or Wait]
	Dispatch --> Confirm[Confirm Delivery]
	Confirm --> End[End]
```

### Passo 2: Inserir Passos Paralelos
- O nó Manage precisa iniciar verificações de clima e condições das estradas além do inventário.
- Adicione dois novos nós:
	- CheckWeather[Check Weather]
	- CheckRoads[Check Road Conditions]
- Conecte Manage a esses novos nós:
	- Manage --> CheckWeather
	- Manage --> CheckRoads

Agora, Manage terá três setas: Inventory, CheckWeather e CheckRoads.

### Passo 3: Definir Agentes e Bloco Paralelo
- Renomeie os nós de verificação para representar agentes:
	- Inventory[Check Inventory] → InventoryAgent
	- CheckWeather[Check Weather] → WeatherAgent
	- CheckRoads[Check Road Conditions] → RoadAgent
- Agrupe esses três agentes em um subgraph para representar execução paralela:

```mermaid
subgraph Parallel Information Gathering
	InventoryAgent
	WeatherAgent
	RoadAgent
end
```

Inclua esse bloco no seu código.

### Passo 4: Coordenador Central e Fluxo de Informação
- Renomeie Manage para StrategicAgent[Strategic Aid Coordinator].
- O StrategicAgent inicia as verificações paralelas:
	- StrategicAgent --> InventoryAgent
	- StrategicAgent --> WeatherAgent
	- StrategicAgent --> RoadAgent
- Após a execução, cada agente reporta de volta ao StrategicAgent:
	- InventoryAgent --> StrategicAgent
	- WeatherAgent --> StrategicAgent
	- RoadAgent --> StrategicAgent
- O DispatchDecision deve seguir o StrategicAgent após o recebimento das informações:
	- StrategicAgent --> DispatchDecision{Ready to Dispatch?}

### Passo 5: Finalização e Rotulagem
- Renomeie Dispatch para DispatchAgent[Dispatch Agent Executes].
- Confirm[Confirm Delivery] e Replan[Replan or Wait] podem ser mantidos ou renomeados para agentes, se desejar.

### Passo 6: Revisão e Teste
- Visualize o diagrama em mermaid.live.
- Verifique se o StrategicAgent inicia três tarefas paralelas.
- Os resultados dos agentes paralelos retornam ao StrategicAgent antes da decisão de despacho.
- O fluxo deve representar um esforço coordenado de equipe, não apenas uma linha sequencial.

---
Essas instruções guiam a transformação de um fluxo determinístico em um workflow agentic, destacando execução paralela e coordenação entre agentes.
