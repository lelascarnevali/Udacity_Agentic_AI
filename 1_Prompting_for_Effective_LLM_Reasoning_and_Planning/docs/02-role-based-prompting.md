````markdown
# Role-Based Prompting: Guia de Engenharia

> **Nota Técnica**: Este documento compila estratégias de engenharia de prompt focadas na atribuição de personas para especializar a inferência de LLMs. Baseado na análise de experimentos práticos de *Role-Based Prompting* das aulas.

---

## 1. O Conceito de Persona (The Persona Equation)

O *Role-Based Prompting* não é apenas "fingir ser alguém". É uma técnica de modulação da distribuição probabilística do modelo para acessar subconjuntos específicos de conhecimento latente.

### Fórmula Conceitual
$$ P(\text{Response} | \text{Context}) \rightarrow P(\text{Response} | \text{Context}, \text{Role}, \text{Constraints}) $$

Onde a "Persona" atua como um preâmbulo que condiciona o estilo, o vocabulário e a estrutura lógica da resposta.

---

## 2. Componentes da Arquitetura do Prompt

Uma instrução baseada em papéis robusta deve conter três camadas de definição:

| Camada | Função | Exemplo Prático (Transcrição) |
| :--- | :--- | :--- |
| **Role (Papel)** | Define a "identidade" e a qualificação. | *"You are a certified professional organizer."* |
| **Context (Contexto)** | Situação e objetivo. | *"Organize my workspace."* |
| **Constraints (Restrições)** | Limites físicos/lógicos que forçam criatividade. | *"15 minutes, $20 budget, sentimental items."* |

---

## 3. Estudo de Caso: O Paradoxo do Papel Isolado

Uma descoberta crítica dos experimentos (*Source: Lesson 3 Walkthrough*) é que a **atribuição de papel isolada é insuficiente**.

### Experimento: Organizador de Escritório

1.  **Baseline**: *"You are a helpful assistant."*
    *   *Resultado*: Lista genérica de 10 passos (Set goal -> Sort -> Organize).
    *   *Análise*: Funcional, mas pouco inspirada.

2.  **Role-Only**: *"You are a certified professional organizer."*
    *   *Resultado*: **Surpreendentemente similar ao baseline.** A estrutura permaneceu quase idêntica.
    *   *Lição*: Apenas mudar o título do sistema não garante mudança cognitiva profunda sem contexto adicional.

3.  **Role + Constraints**: *"15 mins, $20 budget, limited floor space."*
    *   *Resultado*: Transformação completa. O plano tornou-se compacto (5 pontos), alocou tempo específico para cada tarefa e incluiu "dicas de orçamento" criativas (usar o que já tem em casa).

> **Engineering Insight**: O "Papel" define o *tom*, mas as **"Restrições"** definem a *solução*. Um especialista brilha quando resolve problemas sob limitações, não em vácuo.

---

## 4. Estrutura de Implementação (Python/OpenAI)

Padrão de código para injeção de roles via System Prompt observado na prática:

```python
# Exemplo de Definição de Role para Audiência Técnica
system_prompt = """
You are a best selling writer.
- Always explain your overall reasoning.
- Always conclude with a list of action items.
- Do NOT end with a final question.
"""

user_prompt = """
Generate 10 article ideas about meditation for a TECHNICAL audience (engineers/data scientists).
"""
```

### Resultados de Alta Especificidade
Ao combinar *Role* (Escritor Best-seller) + *Audience Constraint* (Técnica), o modelo gera conexões de domínio cruzado:
*   ❌ *Genérico*: "Benefits of Meditation"
*   ✅ *Role-Based*: "Meditation and Signal Processing: Improving focus and reducing noise in neural data."

---

## 5. Glossário e Métricas

### Avaliação de Eficácia
Como medir se o Role-Based Prompting está funcionando?

*   **Diferenciação Vocabular**: O uso de jargão específico do papel (ex: *signal processing* para engenheiros).
*   **Aderência a Restrições**: Capacidade de navegar limitações complexas propostas (ex: orçamento de $20).

### Termos Chave
*   **System Prompt**: O local arquitetural correto para definir a Persona (separado da instrução do usuário).
*   **Orchestration Layer**: A camada de código que combina o Role (System) e a Task (User) antes do envio à API (ex: função `get_completion`).

---
**Contexto utilizado:**
- **Visual Retention**: Uso de tabelas e blocos de código para fixação.
- **Source Material**: Transcrições da aula prática (Walkthrough de código e Definição de Agente).
- **Conceitos**: Diferença entre Role isolado vs Role com Restrições.

````

---

## 🧪 Exercícios Práticos

Para aplicar os conceitos deste tópico na prática, consulte:

- 📓 [Introdução ao Prompting](../exercises/01-introduction-to-prompting-for-llm-reasoning-and-planning.ipynb) — demonstra o "Paradoxo do Papel Isolado": baseline vs role-only vs role + restrições
- 📓 [Lesson 1: Role-Based Prompting](../exercises/03-lesson-1-role-based-prompting.ipynb) — exercício completo de construção de persona (Albert Einstein) com camadas de atributos, tom e estilo

---

**Tópico anterior:** [O Papel do Prompting em Agentic AI](01-the-role-of-prompting-in-agentic-ai.md)
**Próximo tópico:** [Implementando Role-Based Prompting](03-implementing-role-based-prompting.md)
