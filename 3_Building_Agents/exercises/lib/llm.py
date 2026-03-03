"""Small wrapper around an OpenAI-style client used by the exercises.

This module provides `LLM`, a thin adapter that prepares messages and
optional tool metadata for the underlying HTTP client. It centralizes
payload construction and simple input normalization so exercise code can
invoke models with strings or `BaseMessage` instances.

Notes for readers:
- The wrapper intentionally keeps behavior deterministic (temperature default
  0.0) for reproducible exercise outputs.
- Tools are passed to the model as a compact function schema via
  `Tool.dict()`; the runtime selects `tool_choice: auto` when tools exist.
"""

import os
from typing import List, Optional, Dict, Any
from openai import OpenAI
from lib.messages import (
    AnyMessage,
    AIMessage,
    BaseMessage,
    UserMessage,
)
from lib.tooling import Tool


class LLM:
    """Lightweight LLM client adapter.

    Responsibilities:
    - Resolve API key (explicit parameter or `OPENAI_API_KEY`).
    - Choose a specialized base URL when a Vocarum key is detected.
    - Build chat payloads including optional function/tool metadata.
    - Normalize input types (str, BaseMessage, or list of BaseMessage).
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        tools: Optional[List[Tool]] = None,
        api_key: Optional[str] = None
    ):
        self.model = model
        self.temperature = temperature

        # Resolve key: explicit param or env var
        resolved_key = api_key or os.environ.get("OPENAI_API_KEY", "")

        # Configure Vocarum endpoint if using Vocarum API key
        if resolved_key.startswith('voc-'):
            self.client = OpenAI(
                api_key=resolved_key,
                base_url="https://openai.vocareum.com/v1"
            )
        else:
            # When no key is available, OpenAI client accepts None and will
            # error later when a request is attempted — that's fine for
            # exercises that expect an API-backed run.
            self.client = OpenAI(api_key=resolved_key if resolved_key else None)

        # Tools indexed by name for convenient registration/lookup.
        self.tools: Dict[str, Tool] = {
            tool.name: tool for tool in (tools or [])
        }

    def register_tool(self, tool: Tool):
        """Register a `Tool` instance so it's included in request payloads.

        Typical use: `llm.register_tool(tool)` where `tool` is produced via the
        `@tool` decorator in `lib.tooling`.
        """

        self.tools[tool.name] = tool

    def _build_payload(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        """Construct the chat completion payload expected by the client.

        Converts `BaseMessage` objects to their JSON-safe dict form and
        appends tool/function schemas when any tools are registered.
        """

        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [m.dict() for m in messages],
        }

        if self.tools:
            payload["tools"] = [tool.dict() for tool in self.tools.values()]
            payload["tool_choice"] = "auto"

        return payload

    def _convert_input(self, input: Any) -> List[BaseMessage]:
        """Normalize input into a list of `BaseMessage` instances.

        Accepts a raw string (becomes a `UserMessage`), a single `BaseMessage`,
        or a pre-built list of `BaseMessage` instances. Raises `ValueError` for
        unsupported input types to make errors explicit for exercises/tests.
        """

        if isinstance(input, str):
            return [UserMessage(content=input)]
        elif isinstance(input, BaseMessage):
            return [input]
        elif isinstance(input, list) and all(isinstance(m, BaseMessage) for m in input):
            return input
        else:
            raise ValueError(f"Invalid input type {type(input)}.")

    def invoke(self, input: str | BaseMessage | List[BaseMessage]) -> AIMessage:
        """Invoke the model and return an `AIMessage` instance.

        The returned `AIMessage` contains the model's textual content and any
        structured `tool_calls` produced by the model. Callers may examine
        `tool_calls` to decide whether to execute a function/tool.
        """

        messages = self._convert_input(input)
        payload = self._build_payload(messages)
        response = self.client.chat.completions.create(**payload)
        choice = response.choices[0]
        message = choice.message

        return AIMessage(
            content=message.content,
            tool_calls=message.tool_calls
        )
