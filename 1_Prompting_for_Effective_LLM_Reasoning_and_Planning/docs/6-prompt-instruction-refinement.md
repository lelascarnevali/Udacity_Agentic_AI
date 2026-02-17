# Avaliação e Refinamento de Instruções (Prompt Optimization)

> **Nota Técnica**: Engenharia de Prompt não é apenas escrita, é um processo iterativo de *debugging* e otimização. Este guia detalha a metodologia científica para testar e refinar instruções (PromptRefinement), transformando saídas genéricas em respostas de alta precisão.

---

## 1. Anatomia do Prompt (Review)

Um prompt otimizado é composto por cinco engrenagens ajustáveis. Alterar qualquer uma altera o resultado final.

| Componente | Função T écnica | Exemplo (Pirate Ship) |
| :--- | :--- | :--- |
| **Role** | Define a distribuição latente (Persona). | *"Act as a pirate."* |
| **Task** | O objetivo funcional. | *"Respond only to questions about your ship."* |
| **Output Format** | Estrutura de dados da resposta. | *"Output sentences in Markdown."* |
| **Examples** | Few-Shot Learning (Padrões). | *"Q: 1+1? A: Me knows not!"* |
| **Context** | Base de conhecimento (RAG/Static). | *"Ship name: Neptune’s Fury."* |

---

## 2. Metodologia de Ajuste Sistemático (Tuning)

Tal qual afinar um instrumento, a mudança deve ser isolada para medir impacto (*A/B Testing* mental).

### Estudo de Caso: Recomendação de Prato (New Orleans)
**Meta**: Prato local único, foco em sabor, sem nome de restaurante, <75 palavras.

#### Rodada 1: Modificando o *Role*
*   **Prompt A (Cheerful Food Blogger)**: *"Ready for a taste adventure? Picture this..."*
    *   *Resultado*: Entusiasta, acessível.
*   **Prompt B (High-Dining Critic)**: *"Seek out Yakamein, the city's soulful answer to noodle soup..."*
    *   *Resultado*: Sofisticado, vocabulário complexo ("connoisseur").

#### Rodada 2: Modificando *Constraints* (Task)
*   **Constraint**: *"15 words or less."*
*   **Resultado**: *"Spice lover? Taste explosive Viet-Cajun crawfish – garlicky, buttery, fiery fusion magic awaits!"* (Extremamente denso).

#### Rodada 3: Modificando *Output Format*
*   **Constraint**: *"JSON format {"dish_title": ..., "description": ...}"*
*   **Resultado**: Ideal para integração via código (API parsing).

---

## 3. Melhoria Iterativa (The Refinement Loop)

O ciclo de vida de um prompt não termina na primeira execução.

### Comparativo: A Importância dos Detalhes

| Draft | Prompt | Resultado (Análise) |
| :--- | :--- | :--- |
| **Draft 1** (Baseline) | *"Write a post about EverGreen cup."* | ❌ **Genérico**: "Check out this cup." Sem engajamento, sem valor claro. |
| **Draft 2** (+Context) | *"It's durable, eco-friendly..."* | ⚠️ **Seco**: Inclui fatos, mas o tom é enciclopédico. |
| **Draft 3** (+Role + Constraints) | *"You are an enthusiastic manager. Use emojis. CTA."* | ✅ **Otimizado**: "Hey eco-coffee lovers! ✨" Conecta fatos com emoção e ação. |

---

## 4. Otimização para Agentes (Agentic Systems)

Quando o prompt é parte de um sistema agêntico (ReAct), o **Refinamento de Ferramentas** é crítico. O LLM não adivinha como usar uma API; ele lê a descrição que você escreve.

### Code Pattern: Refinando Definições de Ferramentas
Uma descrição pobre leva a alucinações. Uma descrição rica age como "few-shot learning".

**❌ Poor Tool Description**
```python
tools = [
    {"name": "search_db", "description": "Searches the database."}
]
# O LLM não sabe O QUE buscar, nem o formato da query.
```

**✅ Optimized Tool Description**
```python
tools = [
    {
        "name": "search_patient_records",
        "description": "Searches for patient history by ID. Returns JSON with allergies and past visits.",
        "parameters": {"patient_id": "Format: 'PAT-1234'"}
    }
]
# O LLM sabe exatamente O QUE entra e O QUE sai.
```

---

## 5. Armadilhas Comuns (Common Pitfalls)

Evite estes erros frequentes que degradam a performance:

1.  **Ambiguidade**: Instruções vagas ("Escreva algo legal") levam a resultados imprevisíveis. Modelos futuros não saberão das instruções que você *pensou* mas não escreveu.
2.  **Contexto Balanceado**:
    *   *Pouco Contexto*: Alucinação (inventar fatos).
    *   *Muito Contexto*: "Lost in the Middle" (o modelo esquece instruções conflitantes ou irrelevantes).
3.  **Expectativa Mágica**: O modelo é probabilístico, não onisciente. Ele não "entende" sua intenção implícita; ele segue sua instrução explícita.
4.  **Adversarial Risk**: Em sistemas públicos, prompts mal definidos podem sofrer *Injection* (usuário sobrescreve as instruções). Restrições fortes ajudam a evitar isso.

---

## 6. Checklist de Refinamento

Antes de deployar um prompt em produção:
1.  [ ] **Clareza**: A tarefa pode ser interpretada de outra forma?
2.  [ ] **Constraints**: Limitei o tamanho/formato?
3.  [ ] **Few-Shot**: Dei exemplos de *bad* vs *good* response?
4.  [ ] **Borda**: Testei com inputs vazios ou adversariais?

> **Engenharia de Software**: Trate o Prompt como Código. Teste, versão, refine.

---
**Contexto utilizado:**
- **Skills:** `create-study-guide`.
- **Source 1:** Transcrições (`Prompt_Instruction_Refinement...Subtitles`) focadas em "Systematic Adjustment" e "Common Pitfalls".
- **Source 2:** Exemplos do Usuário (NOLA Dish, Social Media Post) usados para demonstrar o ciclo de iteração.
- **Conceitos:** Prompt Components, Iterative Refinement, A/B Testing of Prompts.
