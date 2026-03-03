"""Lightweight message models used by the exercises.

This module provides compact, serializable message classes that represent
the common roles in agent pipelines: `system`, `user`, `assistant` (AI), and
`tool`. Each model focuses on a minimal payload (`content`) and exposes a
`dict()` helper that returns a JSON-safe mapping suitable for logging or
sending to an LLM/agent runtime.

Maintainability notes:
- Keep messages small — prefer `content` over large nested structures.
- `AIMessage.tool_calls` may contain richer objects; this module serializes
    only the minimal fields downstream consumers need (id, type,
    function.name, function.arguments).
"""

from pydantic import BaseModel
from typing import Optional, Union, List, Dict, Any, Literal


class BaseMessage(BaseModel):
    """Base message shared by all specific role models.

    A minimal message container with a textual `content` field. Subclasses
    add a `role` literal to indicate the message origin.

    Attributes:
        content: Optional[str] -- textual payload of the message (default "").
    """

    content: Optional[str] = ""

    def dict(self) -> Dict:
        """Return a JSON-safe dict representation of the message.

        Uses Pydantic's `model_dump` with `exclude_none=True` to omit unset
        fields, producing a compact mapping safe for JSON serialization.

        Returns:
            dict: A JSON-serializable representation of the message.
        """

        return self.model_dump(mode="json", exclude_none=True)


class SystemMessage(BaseMessage):
    """Message originating from system-level context (instructions/config).

    The `role` field is set to the literal "system".
    """

    role: Literal["system"] = "system"


class UserMessage(BaseMessage):
    """Message produced by a human user (user input / prompt).

    The `role` field is set to the literal "user".
    """

    role: Literal["user"] = "user"


class ToolMessage(BaseMessage):
    """Message emitted by a tool during execution.

    Attributes:
        tool_call_id: str -- unique id of the tool invocation (required).
        name: Optional[str] -- optional human-friendly tool name.

    The `role` field is set to the literal "tool".
    """

    role: Literal["tool"] = "tool"
    tool_call_id: str
    name: Optional[str] = None


class AIMessage(BaseMessage):
    """Assistant/agent message with optional tool-call metadata.

    `AIMessage` represents responses produced by an assistant or agent. It may
    include `tool_calls`, a list of objects describing tool invocations
    returned by the model. The library serializes only a compact subset of
    each tool call (id, type, function.name, function.arguments) for logging
    and for decision-making about invoking actual tool implementations.
    """

    role: Literal["assistant"] = "assistant"
    tool_calls: Optional[List[Any]] = None

    def dict(self) -> Dict:
        """Return a JSON-safe dict for the AI message, including normalized
        `tool_calls` when present.

        The default Pydantic dump excludes the `tool_calls` field so the
        method can control serialization shape. When `tool_calls` exists each
        entry is mapped to a minimal dict with the keys `id`, `type` and
        a `function` object containing `name` and `arguments`.

        Returns:
            dict: JSON-serializable mapping representing the AI message and
                any normalized tool call metadata.
        """

        base = self.model_dump(mode="json", exclude_none=True, exclude={"tool_calls"})
        if self.tool_calls:
            # Normalize tool call objects to a compact dict form.
            base["tool_calls"] = [
                {
                    "id": getattr(tc, "id", None),
                    "type": getattr(tc, "type", None),
                    "function": {
                        "name": getattr(getattr(tc, "function", None), "name", None),
                        "arguments": getattr(getattr(tc, "function", None), "arguments", None),
                    },
                }
                for tc in self.tool_calls
            ]
        return base


AnyMessage = Union[
    SystemMessage,
    UserMessage,
    AIMessage,
    ToolMessage,
]
