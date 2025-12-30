"""Todo data models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TodoStatus(str, Enum):
    """Todo status enum."""
    PENDING = "pending"
    DONE = "done"


@dataclass
class Todo:
    """Todo item model."""

    id: int
    title: str
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            status=TodoStatus(data.get("status", TodoStatus.PENDING)),
            created_at=data.get("created_at", datetime.now().isoformat()),
        )
