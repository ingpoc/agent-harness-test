"""JSON file storage backend with semantic ID generation."""

import json
from pathlib import Path
from typing import List, Optional

from todo_cli.models import Todo, Status


class TodoStorage:
    """JSON file storage for todos with semantic ID generation."""

    def __init__(self, file_path: Path = Path.home() / ".todos.json") -> None:
        """Initialize storage with file path."""
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Create storage file if it doesn't exist or is empty."""
        if not self.file_path.exists():
            self.file_path.write_text("[]")
        elif self.file_path.stat().st_size == 0:
            self.file_path.write_text("[]")

    def _load(self) -> List[dict]:
        """Load todos from JSON file."""
        content = self.file_path.read_text()
        if not content.strip():
            return []
        return json.loads(content)

    def _save(self, todos: List[dict]) -> None:
        """Save todos to JSON file."""
        self.file_path.write_text(json.dumps(todos, indent=2))

    def _generate_id(self) -> str:
        """Generate semantic ID (F-001, F-002, etc.)."""
        todos = self._load()
        if not todos:
            return "F-001"

        # Extract numeric part from existing IDs
        max_num = 0
        for todo in todos:
            if todo.get("id", "").startswith("F-"):
                try:
                    num = int(todo["id"][2:])
                    max_num = max(max_num, num)
                except (ValueError, IndexError):
                    continue

        return f"F-{max_num + 1:03d}"

    def add(self, todo: Todo) -> Todo:
        """Add a new todo with generated ID."""
        todo.id = self._generate_id()
        todos = self._load()
        todos.append(todo.to_dict())
        self._save(todos)
        return todo

    def list_all(self) -> List[Todo]:
        """Get all todos."""
        todos = self._load()
        return [Todo.from_dict(t) for t in todos]

    def get(self, todo_id: str) -> Optional[Todo]:
        """Get todo by ID."""
        todos = self._load()
        for t in todos:
            if t["id"] == todo_id:
                return Todo.from_dict(t)
        return None

    def update(self, todo_id: str, **kwargs) -> Optional[Todo]:
        """Update todo fields."""
        todos = self._load()
        for i, t in enumerate(todos):
            if t["id"] == todo_id:
                # Update allowed fields
                if "status" in kwargs:
                    t["status"] = kwargs["status"].value
                if "title" in kwargs:
                    t["title"] = kwargs["title"]
                if "description" in kwargs:
                    t["description"] = kwargs["description"]
                self._save(todos)
                return Todo.from_dict(t)
        return None

    def delete(self, todo_id: str) -> bool:
        """Delete todo by ID."""
        todos = self._load()
        original_len = len(todos)
        todos = [t for t in todos if t["id"] != todo_id]
        if len(todos) < original_len:
            self._save(todos)
            return True
        return False

    def filter_by_status(self, status: Status) -> List[Todo]:
        """Filter todos by status."""
        todos = self._load()
        return [Todo.from_dict(t) for t in todos if t["status"] == status.value]
