"""Output parsers for agent/AI messages.

This module contains focused, side-effect-free parser helpers that convert an
`AIMessage` (lib.messages.AIMessage) into Python-native outputs used across
the exercises. Parsers are intentionally small and deterministic; typical
uses include:

- returning raw text (`StrOutputParser`)
- extracting normalized tool-call records (`ToolOutputParser`)
- decoding JSON payloads (`JsonOutputParser`)
- validating/deserializing into a Pydantic model (`PydanticOutputParser`)

Design notes:
- Parsers receive an `AIMessage` and return a primitive, mapping/list, or
    a Pydantic model instance depending on the concrete implementation.
- Docstrings and type hints are the primary documentation for these helpers.
"""

import json
from typing import Any, Type
from abc import ABC, abstractmethod
from pydantic import BaseModel

from lib.messages import AIMessage


class OutputParser(BaseModel, ABC):
    """Abstract base class for output parsers.

    Subclasses must implement `parse(ai_message)` and return a parsed Python
    object. Concrete parsers should be deterministic and avoid side effects.
    """

    @abstractmethod
    def parse(self, ai_message: AIMessage) -> Any:
        """Parse `ai_message` and return a Python-native representation.

        Args:
            ai_message: The `AIMessage` produced by the assistant.

        Returns:
            A parsed object (string, mapping/list, or Pydantic model
            instance) depending on the concrete parser implementation.
        """
        raise NotImplementedError()


class StrOutputParser(OutputParser):
    """Parser that returns the raw `content` string from an `AIMessage`.

    Use this when the assistant response is plain text and no additional
    parsing or validation is required.
    """

    def parse(self, ai_message: AIMessage) -> str:
        return ai_message.content


class ToolOutputParser(BaseModel):
    """Extract and normalize tool-call records from an `AIMessage`.

    Many agent runtimes include a `tool_calls` list on the assistant message.
    This transformer maps each tool call to a compact dict with the keys
    `tool_call_id`, `args` (decoded JSON), and `function_name`.

    Note: inherits from `BaseModel` (not `OutputParser`) so it can be used
    as a lightweight, validated transformer when the full parser interface
    is unnecessary.
    """

    def parse(self, ai_message: AIMessage) -> list[dict]:
        """Normalize `ai_message.tool_calls` into a compact list of dicts.

        Args:
            ai_message: The assistant `AIMessage` expected to contain a
                `tool_calls` iterable. Each tool call object is expected to
                expose `id` and a `function` object with `name` and
                `arguments` (JSON string).

        Returns:
            list[dict]: A list where each entry has the keys:
                - `tool_call_id` (str): the tool invocation id
                - `args` (Any): the decoded JSON arguments
                - `function_name` (str): the function name to invoke

        Raises:
            AttributeError/TypeError: if `ai_message` or its tool call
                entries do not expose the expected attributes.
            json.JSONDecodeError: if `function.arguments` is not valid JSON.
        """

        return [
            {
                "tool_call_id": call.id,
                "args": json.loads(call.function.arguments),
                "function_name": call.function.name,
            }
            for call in ai_message.tool_calls
        ]


class JsonOutputParser(OutputParser):
    """Parse the assistant `content` as JSON and return the decoded value.

    Use when the model is instructed to emit JSON. If the content is not
    valid JSON a `json.JSONDecodeError` will be raised by `json.loads` and
    should be handled by the caller.
    """

    def parse(self, ai_message: AIMessage) -> Any:
        return json.loads(ai_message.content)


class PydanticOutputParser(OutputParser):
    """Validate and deserialize message content into a Pydantic model.

    Attributes:
        model_class: A `pydantic.BaseModel` subclass used to validate and
            construct the returned model instance from the JSON content.

    Example:
        parser = PydanticOutputParser(model_class=MyModel)
        obj = parser.parse(ai_message)

    Notes:
        The parser calls `model_validate_json` on `model_class`; validation
        errors from Pydantic will propagate to the caller.
    """

    model_class: Type[BaseModel]

    def parse(self, ai_message: AIMessage) -> BaseModel:
        return self.model_class.model_validate_json(ai_message.content)
