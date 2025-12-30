"""Todo data model with semantic IDs."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Status(str, Enum):
    """Todo status enum."""

    PENDING = "pending"
    DONE = "done"


@dataclass
class Todo:
    """Todo item with semantic ID."""

    title: str
    description: Optional[str] = None
    status: Status = Status.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    id: str = ""  # Set by storage backend

    def __post_init__(self) -> None:
        """Validate todo after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")

    @property
    def status_symbol(self) -> str:
        """Get status symbol for terminal display."""
        return "✓" if self.status == Status.DONE else "▸"

    def to_dict(self) -> dict:
        """Convert todo to dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """Create todo from dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            status=Status(data["status"]),
            created_at=data["created_at"],
        )
