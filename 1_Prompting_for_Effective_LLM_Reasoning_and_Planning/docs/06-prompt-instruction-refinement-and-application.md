# Refinamento de Instruções de Prompt — Teoria e Aplicação com Python

**Objetivo:** consolidar práticas, workflows e exemplos práticos para projetar, testar e melhorar instruções para LLMs, com um foco prático em experimentos com Python.

$$
\text{Prompt}_{Optimized} = \sum (\text{Papel} + \text{Tarefa} + \text{Contexto} + \text{Formato} + \text{Exemplos}) + \text{Iteração}
$$

---

## 1. Conceito Fundamental

O refinamento de instruções de prompt é o processo sistemático de avaliar, ajustar e testar instruções para alinhar a saída do modelo à intenção do usuário. Trate prompts como código: versionamento, testes e iterações são essenciais.

## 2. Componentes de um Prompt

Um prompt bem-construído costuma ter estas partes:

- Papel (Role): define persona, tom e perspectiva.
- Tarefa (Task): objetivo principal e restrições.
- Formato de saída (Output Format): como a resposta deve ser estruturada (JSON, bullet points, etc.).
- Exemplos (Few-shot): pares de entrada/saída que demonstram comportamento desejado.
- Contexto: informação adicional necessária para a precisão.

Pequenas mudanças em qualquer componente podem causar grandes diferenças no resultado; por isso é importante modificar uma coisa por vez e medir o impacto.

---

## 3. Workflow de Refinamento Sistemático

1. Inicializar com um rascunho de instrução.
2. Executar e avaliar a saída em um conjunto representativo de casos.
3. Isolar a causa do erro (Role, Task, Format, Examples ou Context).
4. Ajustar apenas o componente identificado.
5. Iterar até convergência.

Essa abordagem reduz ruído e facilita entender por que uma mudança funciona (ou não).

---

## 4. Boas Práticas de Prompting

- Seja específico: instruções vagas geram resultados inconsistentes.
- Use papeis/personas para controlar tom e estilo.
- Quebre tarefas complexas em subtarefas menores.
- Especifique formato e restrições (ex.: limite de palavras, tipo de dados de saída).
- Forneça exemplos (2–5) quando precisar de consistência estrutural.
- Evite excesso de contexto irrelevante — prefira conteúdo conciso e necessário.

---

## 5. Armadilhas Comuns

- Ambiguidade: instruções que deixam margem para múltiplas interpretações.
- Contexto insuficiente: o modelo não tem informação que você pressupõe.
- Contexto excessivo/contraditório: instruções conflitantes degradam a qualidade.
- Expectativas irrealistas: LLMs são probabilísticos — valide resultados.

---

## 6. Medir Diferenças entre Versões de Prompt (Experimental)

- Defina métricas: acurácia, consistência de formato, taxas de erro em edge-cases.
- Faça A/B tests entre versões de prompt.
- Use casos de teste representativos (incluindo casos de borda).
- Registre resultados e trate prompts como artefatos versionados.

---

## 7. Exemplo Didático: Recomendação de Prato Local (síntese)

- Se precisar controlar tom, especifique o papel (ex.: "food blogger alegre").
- Para resposta curta, limite palavras e peça parágrafo único.
- Para saída estruturada, solicite JSON com campos definidos.

---

## 8. Aplicação Prática com Python — Caso de Estudo (código e testes)

Neste módulo aplicamos os conceitos para gerar e iterar sobre uma função `process_data` com requisitos evolutivos:

- Entrada: lista de valores e parâmetro `mode` (`'sum' | 'average' | 'median'`).
- Requisitos adicionais (após feedback): ignorar valores não numéricos, retornar `None` para listas vazias, levantar `ValueError` para modos inválidos.

### 8.1 Exemplo de formato de teste (representativo)

```python
# Exemplos de casos de teste
process_data([1, 2, 3, 4, 5], mode='average')  # -> 3.0
process_data([1, 2, 'a', 3], mode='sum')        # -> 6
```

### 8.2 Pseudocódigo do loop de refinamento

1. Gerar código inicial com LLM (prompt simples).
2. Executar bateria de testes automatizados.
3. Formatar feedback com resultados (passed/failed, erros, exceções).
4. Construir prompt de feedback que inclui o código atual e resultados dos testes.
5. Solicitar ao LLM uma versão corrigida (apenas a função).
6. Repetir até que todos os testes passem ou até atingir limite de iterações.

---

## 9. Exemplo Prático: Prompt de Feedback (Padrão)

Ao solicitar melhoria a partir de falhas em testes, siga este template:

- Reafirme o papel: "You are an expert Python developer."
- Inclua `task_description` (requisitos completos, inclusive os novos).
- Insira `initial_code` (implementação atual).
- Insira `initial_feedback` (resultados dos testes, com detalhes).
- Liste requisitos explícitos a corrigir.
- Peça apenas o bloco `def` corrigido, dentro de fences ```python```.

Exemplo curto (esquema):

````markdown
You are an expert Python developer. You wrote a function based on these requirements:

{task_description}

Here is your current implementation:
```python
{initial_code}
```

I've tested your code and here are the results:
{initial_feedback}

Please revise the function so it implements X, Y and Z. Return only the corrected `def` within ```python fences.
````

---

## 10. Validação e Checklist do Validador (subagente)

Antes de aprovar uma versão final, o Validador deve avaliar o conteúdo com base no checklist:

1. Clareza e coerência (0-2)
2. Completude (0-2)
3. Precisão técnica (0-2)
4. Estrutura e formatação (0-2)
5. Alinhamento com as skills e memórias (0-2)

Pontuação mínima para aprovação: 9/10. Se reprovado, o Validador retorna ações específicas de correção.

---

## 11. Exemplo completo: Categorização de Email (aplicação de refinamento)

- Objetivo: Produzir JSON estruturado com `category`, `summary`, `urgency`, `customer_id`.
- Refinamento: transformar resposta livre em formato parseável seguindo regras e exemplos.

Exemplo de saída desejada:

```json
{
  "category": "Billing",
  "summary": "Cobrança em duplicidade no pedido #8675309",
  "urgency": "High",
  "customer_id": "8675309"
}
```

---

## 12. Recomendações Finais

- Automatize testes e registro de resultados para ter observabilidade das mudanças.
- Versione prompts e mantenha histórico de experimentos.
- Use few-shot exemplos cuidadosamente selecionados; prefira representativos, não exaustivos.
- Ao aplicar em produção, adote monitoração e validação adicional para evitar regressões.

---

## Arquivos consultados / alterados

- Lidos: `docs/06-prompt-instruction-refinement.md`, `docs/07-applying-prompt-instruction-refinement-with-python.md`, arquivo de complemento fornecido.
- Criado: `docs/06-07-prompt-instruction-refinement-and-application.md`

