# Guia de Referência: O Papel do Prompting na IA Agêntica

## 1. Conceito Fundamental: O que é um Agente de IA?

Diferente de sistemas de IA tradicionais (regras estáticas) ou LLMs autônomos (geradores de texto), um **Agente de IA** é projetado para **autonomia**, **adaptabilidade** e **interação**.

### Equação do Agente
$$ \text{Agente} = \text{Perceber (Ambiente)} + \text{Decidir (Raciocínio)} + \text{Agir (Ferramentas)} $$

### Diferenciação Chave
| Característica | LLM Autônomo ("Assistente") | Agente de IA ("Parceiro") |
| :--- | :--- | :--- |
| **Foco** | Geração de Texto / Resposta | Execução de Tarefas / Metas |
| **Escopo** | Passivo (espera input) | Ativo (pode agir autonomamente) |
| **Complexidade** | Respostas diretas | Workflows multi-etapas complexos |
| **Capacidades** | Limitado ao treinamento base | Estendido via Ferramentas (Web, APIs, Cálculos) |

---

## 2. Arquitetura de Componentes

Um agente moderno é composto por 5 pilares essenciais:

1.  **🧠 LLM (Cérebro):** Motor de raciocínio. Processa linguagem, planeja e decide.
2.  **🛠️ Ferramentas (Tools):** "Braços e Pernas" do agente. APIs, buscas, cálculos, acesso a banco de dados.
    *   *Permite interagir com o mundo real (digital/físico) e acessar dados em tempo real.*
3.  **📝 Instruções:** "Código de Conduta". System Prompts que definem persona, limites e diretrizes.
4.  **💾 Memória:**
    *   *Curto Prazo:* Contexto da conversa atual.
    *   *Longo Prazo:* Histórico de interações e aprendizado.
5.  **⚙️ Orquestração (Runtime):** O ambiente que executa o loop de pensamento, chama as ferramentas e processa as respostas.

> **Cenário Prático:** Para responder "Posso comprar esse laptop com meu saldo atual?", um LLM falha (não tem dados privados). Um Agente usa uma **Tool** (API do Banco) para buscar o saldo e então raciocina sobre a resposta.

---

## 3. O Poder do Prompting: "Programando" o Modelo

**Prompting** não é apenas fazer perguntas estúpidas; é o método de **programação** do comportamento do agente. Transforma poder de computação bruto em utilidade específica.

### Decomposição de Tarefas (Planning)
Agentes usam prompting para quebrar problemas complexos (ex: "Quero um reembolso") em passos lógicos:
1.  **Identificar:** Verificar histórico de compra.
2.  **Verificar:** Consultar política de devolução.
3.  **Avaliar:** Analisar motivo do cliente.
4.  **Decidir:** Aprovar/negar com base nos dados.

---

## 4. Engenharia de Prompts: Pattern de Refinamento Iterativo

A prática recomendada para obter resultados de alta qualidade não é tentar acertar no "zero-shot", mas sim iterar.

### Fluxo de Refinamento (Estudo de Caso: Organização)

1.  **Baseline Prompt:** *"Dê-me um plano."*
    *   ⚠️ **Resultado:** Genérico, pouco acionável.
2.  **Iteração 1 (+Role):** *"Você é um Organizador Profissional."*
    *   ⚠️ **Resultado:** Melhor tom, mas ainda genérico. Papel por si só não resolve falta de contexto.
3.  **Iteração 2 (+Constraints & Context):** *"...Tenho 15 min, $20, espaço limitado, foco em itens sentimentais."*
    *   ✅ **Resultado:** Otimizado. Plano compacto, alocado por tempo, focado nas restrições reais.

### 🔑 Regra de Ouro
> **Melhor Contexto + Melhores Restrições = Melhor Raciocínio.**
> Não confie apenas no modelo "adivinhar" o que você precisa. Seja explícito sobre **tempo**, **formato**, **restrições** e **objetivos**.

---

## 5. Resumo das Ferramentas Cognitivas

Ao interagir com Agentes, use estas três alavancas para pilotar o comportamento:

1.  **Design Estratégico:** Crie instruções para guiar até um *formato de saída* específico.
2.  **Transparência (Chain-of-Thought):** Peça para o modelo "explicar passo a passo" ou "mostrar o trabalho". Isso melhora a coerência lógica.
3.  **Refinamento Sistemático:** Comece simples, avalie a saída, adicione restrições, repita.

