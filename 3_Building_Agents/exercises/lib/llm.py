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
            self.client = OpenAI(api_key=resolved_key if resolved_key else None)

        self.tools: Dict[str, Tool] = {
            tool.name: tool for tool in (tools or [])
        }

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool

    def _build_payload(self, messages: List[BaseMessage]) -> Dict[str, Any]:
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
        if isinstance(input, str):
            return [UserMessage(content=input)]
        elif isinstance(input, BaseMessage):
            return [input]
        elif isinstance(input, list) and all(isinstance(m, BaseMessage) for m in input):
            return input
        else:
            raise ValueError(f"Invalid input type {type(input)}.")

    def invoke(self, input: str | BaseMessage | List[BaseMessage]) -> AIMessage:
        messages = self._convert_input(input)
        payload = self._build_payload(messages)
        response = self.client.chat.completions.create(**payload)
        choice = response.choices[0]
        message = choice.message

        return AIMessage(
            content=message.content,
            tool_calls=message.tool_calls
        )
