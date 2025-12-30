"""Todo storage backend using JSON file."""
import json
from pathlib import Path
from typing import List, Optional

from todo_cli.models import Todo, TodoStatus


class TodoStorage:
    """JSON file storage for todos."""

    def __init__(self, filepath: str = "todos.json"):
        """Initialize storage with file path."""
        self.filepath = Path(filepath)
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Ensure storage file exists."""
        if not self.filepath.exists():
            self.filepath.write_text("[]")

    def _load(self) -> List[dict]:
        """Load todos from file."""
        content = self.filepath.read_text()
        if not content.strip():
            return []
        return json.loads(content)

    def _save(self, todos: List[dict]) -> None:
        """Save todos to file."""
        self.filepath.write_text(json.dumps(todos, indent=2))

    def _get_next_id(self) -> int:
        """Get next available ID."""
        todos = self._load()
        if not todos:
            return 1
        return max(t["id"] for t in todos) + 1

    def create(self, title: str, description: Optional[str] = None) -> Todo:
        """Create a new todo."""
        todo_id = self._get_next_id()
        todo = Todo(id=todo_id, title=title, description=description)
        todos = self._load()
        todos.append(todo.to_dict())
        self._save(todos)
        return todo

    def get_all(self, status: Optional[TodoStatus] = None) -> List[Todo]:
        """Get all todos, optionally filtered by status."""
        todos = self._load()
        if status:
            todos = [t for t in todos if t["status"] == status.value]
        return [Todo.from_dict(t) for t in todos]

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get todo by ID."""
        todos = self._load()
        for t in todos:
            if t["id"] == todo_id:
                return Todo.from_dict(t)
        return None

    def update(self, todo_id: int, **kwargs) -> Optional[Todo]:
        """Update todo by ID."""
        todos = self._load()
        for i, t in enumerate(todos):
            if t["id"] == todo_id:
                # Update fields
                for key, value in kwargs.items():
                    if key == "status" and isinstance(value, TodoStatus):
                        value = value.value
                    t[key] = value
                self._save(todos)
                return Todo.from_dict(t)
        return None

    def delete(self, todo_id: int) -> bool:
        """Delete todo by ID."""
        todos = self._load()
        original_len = len(todos)
        todos = [t for t in todos if t["id"] != todo_id]
        if len(todos) < original_len:
            self._save(todos)
            return True
        return False
