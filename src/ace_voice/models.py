from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4


Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Message:
    role: Role
    content: str


@dataclass
class ConversationSession:
    session_id: str = field(default_factory=lambda: str(uuid4()))
    business_id: str | None = None
    agent_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    messages: list[Message] = field(default_factory=list)

    def add_user_message(self, content: str) -> None:
        if not content.strip():
            raise ValueError("A conversation turn cannot be empty")
        self.messages.append(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        if not content.strip():
            raise ValueError("An assistant response cannot be empty")
        self.messages.append(Message(role="assistant", content=content))

    def model_messages(self) -> tuple[Message, ...]:
        return tuple(self.messages)
