````markdown
# Implementando Role-Based Prompting: De Ator a Especialista

> **Nota Técnica**: Este guia explora a implementação prática de personas em Python, diferenciando entre "Personas Criativas" (Atores) e "Personas Profissionais" (Especialistas). Baseado nos exercícios de simulação histórica (Einstein) e análise de segurança (Phishing).

---

## 1. O Espectro da Persona (The Persona Spectrum)

Na engenharia de prompt, as personas servem a dois propósitos distintos. É crucial distinguir qual "modo" você está ativando no modelo:

| Tipo | **The Actor (O Ator)** | **The Expert (O Especialista)** |
| :--- | :--- | :--- |
| **Objetivo** | Simulação, Entretenimento, Empatia. | Precisão, Análise Técnica, Segurança. |
| **Foco** | *Tone & Style* (Tom e Estilo). | *Constraints & Reasoning* (Restrições e Raciocínio). |
| **Exemplo** | Albert Einstein explicando relatividade. | Analista de Cibersegurança avaliando um email. |
| **Métrica** | Autenticidade Histórica/Emocional. | Acurácia, Estrutura e "Safety". |

---

## 2. Implementação 1: The Actor (Simulação Histórica)
*Source: Lesson 1 Demo (Albert Einstein)*

Para criar um ator convincente, utilizamos a técnica de **Camadas de Atributos** (*Attribute Layering*). Não basta dizer "Seja Einstein".

### Padrão de Código (Layering)
```python
# 1. Baseline
base_system_prompt = "Pretend you are Albert Einstein."

# 2. Persona Attributes (Personality & Context)
attributes = """
- Personality: Curious, humble yet confident.
- Context: Speak as if in 1950. Only discuss info known by then.
"""

# 3. Tone & Style (The "Vibe")
tone_style = """
- Speak in a warm, grandfatherly manner.
- Use phrases like "You see" and "Imagine if you will".
- Occasionally make self-deprecating jokes about your hair.
"""

# Final Assembly
full_system_prompt = base_system_prompt + attributes + tone_style
```

### Resultado Prático
*   **Prompt Genérico:** "Relativity is a theory..."
*   **Prompt com Persona:** "Yes, relativity. Such a delightful topic... Though I must admit, my hair has become quite the wild conductor's wig over the years." (Incorpora estilo e humor instruídos).

---

## 3. Implementação 2: The Expert (Análise Profissional)
*Source: Phishing Email Case Study*

Para especialistas, o foco muda de "quem você é" para "como você pensa". O objetivo é evitar respostas genéricas de "assistente útil" e forçar rigor técnico.

### Estudo de Caso: Análise de Email Suspeito

#### 🔴 The Generic Assistant
*   **Input:** "Analyze this email for safety."
*   **Output:** "Looks like phishing. Don't click."
*   **Problema:** Correto, mas superficial. Falta autoridade e estrutura.

#### 🟢 The Cybersecurity Analyst
O prompt de especialista define **rigor de processo**.

```python
system_prompt_analyst = """
You are a senior Cybersecurity Analyst providing a formal threat assessment.
Tone: Objective, Cautious, Precise.

Procedure:
1. State overall assessment (e.g., "High-Confidence Phishing").
2. NO speculation or casual language.
3. List Red Flags as bullet points with technical explanations.
4. Conclude with actionable recommendation.
"""
```

### Comparative Analysis Table

| Feature | Generic Assistant | Cybersecurity Analyst |
| :--- | :--- | :--- |
| **Veredito** | "Parece golpe" | "High-Confidence Phishing Attempt" |
| **Evidência** | Vaga ("Link suspeito") | Específica ("Sender Address Spoofing: subdomain support-update") |
| **Ação** | "Não clique" | "Delete immediately. Navigate manually to official site." |
| **Engenharia** | Zero-Shot genérico | Role + Chain of Thought (Procedure 1-4) |

---

## 4. Conclusão de Engenharia

Ao implementar *Role-Based Prompting* em Python:
1.  **Iteração é Chave:** Comece com o Baseline, adicione Atributos, refine com Estilo/Restrições.
2.  **Validação de "Ground Truth":** Para personas históricas, poderíamos validar medindo frequência de palavras vs dataset real do autor. Para especialistas, validamos contra checklists técnicos reais.
3.  **Segurança:** Personas de especialistas (como Cibersegurança) aumentam a segurança da resposta ao impor protocolos rígidos que um assistente genérico pode ignorar.

---
**Contexto utilizado:**
- **Skills:** `create-study-guide` (Engenharia > Prosa).
- **Source 1 (Arquivo):** `1 - C1l1 Lesson1demo V2 - lang_en-us.srt` (Exemplo Einstein/Ator).
- **Source 2 (User Text):** Exemplo Phishing/Expert.
- **Conceitos:** Attribute Layering, Generic vs Expert comparison.

````

---

## 🧪 Exercícios Práticos

Para aplicar os conceitos deste tópico na prática, consulte:

- 📓 [Lesson 1: Role-Based Prompting — Historical Figure Interviewer](../exercises/03-lesson-1-role-based-prompting.ipynb) — implementação completa do padrão "The Actor": persona de Einstein com attribute layering (baseline → persona → tone/style → Q&A interativo)

---

**Tópico anterior:** [Role-Based Prompting: Guia de Engenharia](02-role-based-prompting.md)
**Próximo tópico:** [Chain-of-Thought & ReAct](04-chain-of-thought-and-react-prompting.md)
