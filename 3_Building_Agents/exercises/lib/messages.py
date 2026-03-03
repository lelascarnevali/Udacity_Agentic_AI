from pydantic import BaseModel
from typing import Optional, Union, List, Dict, Any, Literal


class BaseMessage(BaseModel):
    content: Optional[str] = ""

    def dict(self) -> Dict:
        return self.model_dump(mode="json", exclude_none=True)


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"


class UserMessage(BaseMessage):
    role: Literal["user"] = "user"


class ToolMessage(BaseMessage):
    role: Literal["tool"] = "tool"
    tool_call_id: str
    name: Optional[str] = None


class AIMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"
    tool_calls: Optional[List[Any]] = None

    def dict(self) -> Dict:
        base = self.model_dump(mode="json", exclude_none=True, exclude={"tool_calls"})
        if self.tool_calls:
            base["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
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
