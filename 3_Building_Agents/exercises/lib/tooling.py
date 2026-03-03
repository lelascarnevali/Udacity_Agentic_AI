"""Utilities for exposing Python callables as function-like tools.

This module provides a small `Tool` adapter that introspects a Python
callable (signature and type hints) and produces a JSON-schema-like function
description suitable for model function-calling integrations.

Primary responsibilities:
- Infer a compact JSON schema for function parameters from type hints.
- Provide a callable wrapper (`Tool`) that can be invoked directly or via
  the `execute()` API which accepts a dict of arguments.
- Offer the `@tool` decorator for convenient declaration of tools.
"""

import inspect
import datetime
from typing import (
    Callable, Any, get_type_hints, get_origin, get_args,
    Literal, Optional, Union, List, Dict
)
from functools import wraps


class Tool:
    """Adapter that exposes a Python callable as a function/tool schema.

    The adapter captures:
    - `name`: function name (or provided override)
    - `description`: docstring of the function when available
    - `parameters`: a list of argument schemas inferred from type hints

    This small abstraction is useful for exercises that demonstrate model
    function-calling or tool invocation patterns.
    """

    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.func = func
        self.name = name or func.__name__
        self.description = description or inspect.getdoc(func)
        # Capture signature and type hints for parameter schema generation
        self.signature = inspect.signature(func, eval_str=True)
        self.type_hints = get_type_hints(func)

        self.parameters = [
            self._build_param_schema(key, param)
            for key, param in self.signature.parameters.items()
        ]

    def _build_param_schema(self, name: str, param: inspect.Parameter):
        """Build a small schema for a single parameter.

        Returns a dict containing the parameter name, its inferred JSON schema,
        and whether it is required.
        """

        param_type = self.type_hints.get(name, str)
        schema = self._infer_json_schema_type(param_type)
        return {
            "name": name,
            "schema": schema,
            "required": param.default == inspect.Parameter.empty
        }

    def _infer_json_schema_type(self, typ: Any) -> dict:
        """Map Python type hints to a compact JSON-schema-like mapping.

        Handles `Literal` (as enums), `Union`/`Optional`, lists and dicts, and
        falls back to string for unknown types. Date/datetime are represented as
        strings for simplicity (ISO format expected at runtime).
        """

        origin = get_origin(typ)

        # Handle Literal (enums)
        if origin is Literal:
            return {
                "type": "string",
                "enum": list(get_args(typ))
            }

        # Handle Optional[T]
        if origin is Union:
            args = get_args(typ)
            non_none = [arg for arg in args if arg is not type(None)]
            if len(non_none) == 1:
                return self._infer_json_schema_type(non_none[0])
            return {"type": "string"}  # fallback

        # Handle collections
        if origin is list:
            return {
                "type": "array",
                "items": self._infer_json_schema_type(get_args(typ)[0] if get_args(typ) else str)
            }

        if origin is dict:
            return {
                "type": "object",
                "additionalProperties": self._infer_json_schema_type(get_args(typ)[1] if get_args(typ) else str)
            }

        # Primitive mappings
        mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            datetime.date: "string",
            datetime.datetime: "string",
        }

        return {"type": mapping.get(typ, "string")}

    def dict(self) -> dict:
        """Return a compact function schema suitable for model function-calling.

        The structure matches the small subset used in the exercises: a
        top-level type of `function` with a `function` object that lists
        `parameters` in JSON-schema style.
        """

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        param["name"]: param["schema"]
                        for param in self.parameters
                    },
                    "required": [
                        param["name"] for param in self.parameters if param["required"]
                    ],
                    "additionalProperties": False
                }
            }
        }

    def __call__(self, *args, **kwargs):
        """Allow the `Tool` to be invoked like the original function.

        This forwards positional and keyword args directly to the wrapped
        callable, making `Tool` usable in test code as a drop-in wrapper.
        """

        return self.func(*args, **kwargs)

    def execute(self, args: Dict[str, Any]) -> Any:
        """Execute the tool with the provided arguments mapping.

        Typical runtime usage: `tool.execute({'x': 1, 'y': 2})`.
        """

        return self.func(**args)

    def __repr__(self):
        return f"<Tool name={self.name} params={[p['name'] for p in self.parameters]}>"

    @classmethod
    def from_func(cls, func: Callable):
        """Convenience constructor from a raw callable."""

        return cls(func)



def tool(func=None, *, name: str = None, description: str = None):
    """Decorator to expose a function as a `Tool` instance.

    Usage:
        @tool
        def my_tool(x: int) -> int:
            return x + 1

        # or
        @tool(name="increment")
        def my_tool(x: int) -> int:
            return x + 1

    The decorator returns a `Tool` instance which can be registered with an
    `LLM` or inspected to produce a function schema.
    """

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return Tool(f, name=name, description=description)
    
    # @tool or @tool(name="foo")
    return wrapper(func) if func else wrapper