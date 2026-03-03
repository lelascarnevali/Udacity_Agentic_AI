"""Lightweight message models used by the exercises.

This module defines small, serializable message classes that mirror the
typical roles used in agent pipelines: system, user, assistant (AI), and
tool. Models are intentionally minimal: they provide a `dict()` method that
returns a JSON-serializable mapping suitable for logging or sending to an
LLM/agent runtime.

Guidelines for maintainers/readers:
- Keep message payloads small (primarily `content`).
- Extend `AIMessage.tool_calls` objects only with the minimal fields needed
  by downstream tooling (id, type, function.name, function.arguments).
"""

from pydantic import BaseModel
from typing import Optional, Union, List, Dict, Any, Literal


class BaseMessage(BaseModel):
    """Base message shared by all specific role models.

    Attributes:
        content: Optional[str] -- textual payload of the message (default "").
    """

    content: Optional[str] = ""

    def dict(self) -> Dict:
        """Return a JSON-safe dict for the message.

        Uses Pydantic's `model_dump` with `exclude_none=True` to omit unset
        fields. This keeps logs compact and avoids serializing `None` values.
        """

        return self.model_dump(mode="json", exclude_none=True)


class SystemMessage(BaseMessage):
    """Message originating from system-level context (instructions, config)."""

    role: Literal["system"] = "system"


class UserMessage(BaseMessage):
    """Message produced by a human user (user input / prompt)."""

    role: Literal["user"] = "user"


class ToolMessage(BaseMessage):
    """Message emitted by a tool during execution.

    Fields:
        tool_call_id: str -- unique id of the tool invocation (required)
        name: Optional[str] -- optional human-friendly tool name
    """

    role: Literal["tool"] = "tool"
    tool_call_id: str
    name: Optional[str] = None


class AIMessage(BaseMessage):
    """Assistant/agent message.

    Optionally contains `tool_calls`, a list of tool-call objects returned by
    the agent. Those objects are often richer than this library needs; the
    `dict()` method extracts the minimal shape useful for downstream consumers
    (logging, replay, or invoking real tools): id, type and function name/
    arguments.
    """

    role: Literal["assistant"] = "assistant"
    tool_calls: Optional[List[Any]] = None

    def dict(self) -> Dict:
        """Return a JSON-safe dict for the AI message, including tool calls.

        We intentionally exclude the raw `tool_calls` from the base dump to
        control the exact keys serialized for each tool call. If `tool_calls`
        is present, transform each entry into a minimal dictionary with the
        fields consumers expect.
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
