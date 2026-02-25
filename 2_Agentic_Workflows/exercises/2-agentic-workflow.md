## Diagrama Final (Mermaid)

```mermaid
flowchart TD
  Start[Start] --> StrategicAgent[Strategic Aid Coordinator]
  subgraph Parallel Information Gathering
    InventoryAgent[Inventory Agent]
    WeatherAgent[Weather Agent]
    RoadAgent[Road Agent]
  end
  StrategicAgent --> InventoryAgent
  StrategicAgent --> WeatherAgent
  StrategicAgent --> RoadAgent
  InventoryAgent --> StrategicAgent
  WeatherAgent --> StrategicAgent
  RoadAgent --> StrategicAgent
  StrategicAgent --> DispatchDecision{Ready to Dispatch?}
  DispatchDecision -- Yes --> DispatchAgent[Dispatch Agent Executes]
  DispatchDecision -- No --> Replan[Replan or Wait]
  DispatchAgent --> Confirm[Confirm Delivery]
  Confirm --> End[End]
```

---

## Observações
- O StrategicAgent coordena a execução paralela dos agentes.
- Os resultados retornam ao coordenador antes da decisão de despacho.
- O fluxo representa um esforço de equipe, não apenas uma sequência linear.flowchart TD
  Start[Start] --> Manage[Manage Aid Request]
  Manage --> Inventory[Check Inventory]
  Manage --> CheckWeather[Check Weather]
  Manage --> CheckRoads[Check Road Conditions]
  Inventory --> // Placeholder for result flow
  Manage --> DispatchDecision{Ready to Dispatch?}
  DispatchDecision -- Yes --> Dispatch[Dispatch Team]
  DispatchDecision -- No --> Replan[Replan or Wait]
  Dispatch --> Confirm[Confirm Delivery]
  Confirm --> End[End]