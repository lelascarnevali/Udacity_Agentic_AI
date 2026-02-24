# Agent Memory Entry

- **Date:** 2026-02-24
- **Topic:** GPT-5 family and newer — practical usage notes
- **Topics/Tags:** models, gpt5+, reasoning, api, compatibility, chat-completions, responses
- **Source:** Hands-on debugging and testing in `2_Agentic_Workflows/exercises/1-starter.py`

## Context
We explored using newer GPT-5-family models (example: `gpt-5-nano`) on an OpenAI-compatible Vocareum endpoint while updating a starter exercise. Different provider configurations expose model capabilities via either the Responses API or Chat Completions API; parameter names and required fields differ.

## Key Insights (research-backed)
- Reasoning models (GPT-5 family and newer) introduce reasoning tokens and often expose reasoning controls (`reasoning.effort`) in the Responses API. See OpenAI "Reasoning models" guide for details.
- Preferred API: the Responses API is recommended for full reasoning model features (reasoning summaries, reasoning token accounting). However, many provider endpoints still support or prefer Chat Completions for GPT-5-family models; test both.
- Parameter mapping:
  - Responses API: use `reasoning={"effort": "low|medium|high"}` and `max_output_tokens` / `include` as needed.
  - Chat Completions (provider-specific): some endpoints require passing reasoning/verbosity controls in `extra_body` (e.g., `{"reasoning_effort":"minimal","verbosity":"low"}`). This is a provider-specific convention observed in Vocareum.
- Availability: model names and availability vary across providers; always implement an `OPENAI_MODEL` override and a graceful fallback strategy.

## Actionable Rules / Recommendations
- Default behavior in repo code:
  1. Try Responses API with `model` set to the target GPT-5 family model and `reasoning` parameter when the endpoint advertises Responses support.
  2. If Responses returns an "Invalid Service" or the provider indicates Chat-only, fall back to Chat Completions and pass `extra_body` with `reasoning_effort` and `verbosity` as needed.
- Use `reasoning`/`reasoning_effort` conservatively:
  - `minimal`/`low` for short answers and low latency/cost
  - `medium` for balanced reasoning
  - `high` for complex multi-step tasks (be mindful of token usage)
- Reserve ample context window for reasoning-heavy tasks; monitor `usage.output_tokens_details.reasoning_tokens` and set `max_output_tokens` appropriately to avoid incomplete responses.
- Extraction: prefer Response fields in the order of `output_text` (Responses), `output -> content -> text`, then Chat `choices[0].message.content` as fallback.
- Expose `OPENAI_MODEL` env var for easy testing; implement a fallback chain in code to try multiple candidate models if first attempt yields no usable content.

## Minimal examples (adapt to repo client)

Responses API (preferred for reasoning if supported):
```python
response = client.responses.create(
    model="gpt-5",
    reasoning={"effort": "low"},
    input=question,
    max_output_tokens=300,
)
answer = getattr(response, "output_text", None) or ""
```

Chat Completions (fallback / provider-specific):
```python
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "You are an expert assistant."},
        {"role": "user", "content": question},
    ],
    extra_body={"reasoning_effort": "minimal", "verbosity": "low"},
)
answer = response.choices[0].message.content.strip()
```

## References
- OpenAI Reasoning models guide: https://developers.openai.com/docs/guides/reasoning
- Responses API reference: https://developers.openai.com/api/reference/responses
- Chat Completions reference: https://developers.openai.com/api/reference/chat

## Next Actions
- Keep this memory updated when model parameters or API shapes change (e.g., GPT-5.1 -> GPT-5.2). Document provider-specific quirks (Vocareum, internal endpoints).
- Add a small test script in `scripts/` demonstrating automatic fallback: Responses -> Chat with `OPENAI_MODEL` override.

## Tags
gpt5+, reasoning, responses, chat-completions, provider-fallback
