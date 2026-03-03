"""Tooling utilities to expose Python callables as compact, model-ready tools.

This module provides a lightweight `Tool` adapter and the `@tool` decorator
to convert ordinary Python callables into small, JSON-schema-like function
descriptions suitable for LLM function-calling integrations used in the
exercises.

Key behaviors:
- Infer a compact parameter schema from function signatures and type hints
    (supports `Literal`, `Optional`/`Union`, lists, dicts and primitives).
- Represent date/time types as ISO-format strings for runtime interchange.
- Expose a `Tool` wrapper that is callable, provides `execute(args: dict)`,
    and can produce a schema via `Tool.dict()` for registration with an LLM.

Usage example:
        @tool
        def add(x: int, y: int) -> int:
                return x + y

        t = add  # `t` is a Tool instance
        schema = t.dict()  # compact schema suitable for model function-calling

Notes:
- The generated schema is intentionally compact and exercise-focused; it is
    not a full JSON Schema implementation and favors clarity over completeness.
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
        """Initialize the `Tool` wrapper.

        Args:
            func: The underlying callable to expose as a tool.
            name: Optional explicit name to use instead of the function name.
            description: Optional description; defaults to the wrapped function's
                docstring when not provided.
        """

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

        Args:
            name: The parameter name.
            param: The `inspect.Parameter` instance to analyze.

        Returns:
            A dict with keys `name`, `schema` and `required` describing the
            parameter and its inferred JSON-schema-like type mapping.
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

        Args:
            typ: A Python type or typing annotation to convert.

        Returns:
            A dict representing a compact JSON-schema-like type description.

        Notes:
            Supports `Literal`, `Union`/`Optional`, lists, dicts and primitive
            types. Date/time types are represented as strings (ISO-8601).
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

        Returns:
            A dict containing the function schema (name, description, parameters)
            using a compact JSON-schema-like structure used by the exercises.
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
        """Invoke the wrapped callable with the provided arguments.

        Args:
            *args: Positional arguments forwarded to the underlying function.
            **kwargs: Keyword arguments forwarded to the underlying function.

        Returns:
            The value returned by the wrapped function.
        """

        return self.func(*args, **kwargs)

    def execute(self, args: Dict[str, Any]) -> Any:
        """Execute the tool using a mapping of argument names to values.

        Args:
            args: A mapping of parameter names to values to pass to the function.

        Returns:
            The result of invoking the underlying function with the provided
            arguments.

        Example:
            `tool.execute({'x': 1, 'y': 2})`
        """

        return self.func(**args)

    def __repr__(self):
        """Return a concise representation for debugging.

        Returns:
            A short string including the tool name and parameter names.
        """

        return f"<Tool name={self.name} params={[p['name'] for p in self.parameters]}>"

    @classmethod
    def from_func(cls, func: Callable):
        """Create and return a `Tool` instance wrapping `func`.

        Args:
            func: The callable to wrap.

        Returns:
            A `Tool` instance wrapping `func`.
        """

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
        """Return a decorator that converts a callable into a `Tool` instance.

        The wrapper preserves the original function's metadata via
        `functools.wraps` and returns a `Tool` wrapping the function.
        """

        @wraps(f)
        def wrapped(*args, **kwargs):
            """Passthrough wrapper that forwards calls to the original function.

            Preserves the original function's metadata via `functools.wraps` and
            forwards positional and keyword arguments unchanged. The decorator
            ultimately returns a `Tool` instance, so this wrapper is not the
            decorator's final return value; it exists primarily to maintain
            metadata and identical call semantics if invoked directly.
            """

            return f(*args, **kwargs)

        return Tool(f, name=name, description=description)
    
    # @tool or @tool(name="foo")
    return wrapper(func) if func else wrapper