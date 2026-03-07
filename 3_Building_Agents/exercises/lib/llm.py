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
from pydantic import BaseModel
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
        """Create an `LLM` adapter instance.

        Args:
            model: Model identifier passed to the underlying client.
            temperature: Sampling temperature (defaults to 0.0 for
                deterministic exercise outputs).
            tools: Optional list of `Tool` instances to register up-front.
            api_key: Optional API key; when omitted the `OPENAI_API_KEY`
                environment variable is used. Keys prefixed with `voc-`
                switch the client to a Vocarum-compatible base URL.

        The initializer configures the OpenAI client and prepares an
        index of registered `Tool`s keyed by name for payload construction.
        """

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
        """Register a `Tool` for inclusion in subsequent requests.

        Args:
            tool: A `Tool` object (typically created by the `@tool`
                decorator in `lib.tooling`).

        Side effects:
            Adds `tool` to the adapter's `self.tools` mapping keyed by
            `tool.name`, so `_build_payload` will include its schema.
        """

        self.tools[tool.name] = tool

    def _build_payload(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        """Build the request payload sent to the OpenAI-style client.

        Args:
            messages: List of `BaseMessage` instances to include in the
                chat exchange. Each message is converted to a JSON-safe
                dict via its `.dict()` helper.

        Returns:
            A dict containing `model`, `temperature`, and `messages`. If
            tools are registered the payload also contains a `tools`
            entry (list of tool schemas) and `tool_choice: "auto"`.

        Note:
            Temperature is omitted for gpt-5 family models as they don't
            support explicit temperature settings.
        """

        payload = {
            "model": self.model,
            "messages": [m.dict() for m in messages],
        }

        if not self.model.startswith("gpt-5"):
            payload["temperature"] = self.temperature

        if self.tools:
            payload["tools"] = [tool.dict() for tool in self.tools.values()]
            payload["tool_choice"] = "auto"

        return payload

    def _convert_input(self, input: Any) -> List[BaseMessage]:
        """Normalize various input forms into a list of `BaseMessage`.

        Supported inputs:
        - `str`: converted to a single `UserMessage` with `content` set.
        - `BaseMessage`: wrapped in a single-element list.
        - `list` of `BaseMessage`: returned unchanged after validation.

        Raises:
            ValueError: if `input` is not one of the supported types.
        """

        if isinstance(input, str):
            return [UserMessage(content=input)]
        elif isinstance(input, BaseMessage):
            return [input]
        elif isinstance(input, list) and all(isinstance(m, BaseMessage) for m in input):
            return input
        else:
            raise ValueError(f"Invalid input type {type(input)}.")

    def invoke(self, 
               input: str | BaseMessage | List[BaseMessage], 
               response_format: BaseModel = None,) -> AIMessage:
        """Invoke the model and return an `AIMessage` containing the result.

        Args:
            input (str | BaseMessage | List[BaseMessage]): User input or
                pre-built message(s) to send to the model.
            response_format (Optional[BaseModel]): If provided, a Pydantic
                model used to parse structured model responses via the
                beta parsing endpoint.

        Returns:
            AIMessage: object with `content` (str) and optional
                `tool_calls` (structured data) produced by the model.

        Notes:
            When `response_format` is set the adapter uses the beta
            `.parse()` endpoint; otherwise it calls the standard
            `.create()` endpoint. Any `tool_calls` returned by the model
            are preserved on the returned `AIMessage` for callers to
            inspect and (optionally) execute.
        """

        messages = self._convert_input(input)
        payload = self._build_payload(messages)
        if response_format:
            payload.update({"response_format": response_format})
            response = self.client.beta.chat.completions.parse(**payload)
        else:
            response = self.client.chat.completions.create(**payload)
        choice = response.choices[0]
        message = choice.message

        return AIMessage(
            content=message.content,
            tool_calls=message.tool_calls
        )