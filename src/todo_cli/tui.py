"""Interactive Terminal UI using Textual with Amber Terminal aesthetic."""
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Static,
)

from todo_cli.models import Todo, TodoStatus
from todo_cli.storage import TodoStorage


class TodoItem(ListItem):
    """A todo list item widget."""

    def __init__(self, todo: Todo):
        self.todo = todo
        status_color = "green" if todo.status == TodoStatus.DONE else "yellow"
        status_icon = "✓" if todo.status == TodoStatus.DONE else "○"
        super().__init__()
        self.update(f"[{status_color}]▏[/] {status_icon} [bold white]{todo.title}[/]  [dim]{todo.status.value}[/]")


class TodoTui(App):
    """Interactive Todo Terminal UI with Amber Terminal aesthetic."""

    CSS = """
    Screen {
        background: #0a0a0a;
    }
    Header {
        background: #1a1a1a;
        text-style: bold;
        color: #ffb000;
        border: double #ffb000;
        padding: 0 1;
    }
    Header.-touched {
        background: #2a2a2a;
    }
    Horizontal {
        border: double #ffb000;
        padding: 1;
    }
    #input_panel {
        height: 5;
        border: double #ffb000;
        padding: 1;
    }
    Input {
        width: 1fr;
        border: solid #ffb000;
        background: #1a1a1a;
        color: #ffb000;
    }
    Button {
        width: 12;
        background: #1a1a1a;
        border: solid #ffb000;
        color: #ffb000;
        text-style: bold;
    }
    Button:hover {
        background: #ffb000;
        color: #0a0a0a;
    }
    ListView {
        background: #0a0a0a;
    }
    ListItem {
        background: #1a1a1a;
        border: solid #333;
    }
    ListItem.-selected {
        background: #ffb000;
        color: #0a0a0a;
    }
    Label {
        color: #ffb000;
        text-style: bold;
    }
    #status_bar {
        height: 3;
        dock: bottom;
        background: #1a1a1a;
        border: double #ffb000;
        padding: 0 1;
    }
    Static {
        color: #ffb000;
    }
    """

    TITLE = "╔═══════════════════════════════════════╗\n║      ✦ TODO TERMINAL UI ✦             ║\n╚═══════════════════════════════════════╝"

    def __init__(self):
        super().__init__()
        self.storage = TodoStorage()
        self.todos: list[Todo] = []
        self.selected_todo: Optional[Todo] = None

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        with Horizontal():
            with Vertical(id="todo_list"):
                yield Label("╭─ Your Todos ─╮")
                yield ListView(id="todo_list_view")
            with Vertical(id="input_panel"):
                yield Label("╭─ Add Todo ─╮")
                yield Input(placeholder="Enter todo title...", id="title_input")
                yield Input(placeholder="Description (optional)...", id="desc_input")
                with Horizontal():
                    yield Button("Add", variant="primary", id="add_btn")
                    yield Button("Complete", id="complete_btn")
                    yield Button("Delete", id="delete_btn")
        yield Static(id="status_bar")

    def on_mount(self) -> None:
        """Initialize UI on mount."""
        self.refresh_todos()
        self.update_status("Ready • Press 'q' to quit")

    def refresh_todos(self) -> None:
        """Refresh the todo list."""
        self.todos = self.storage.get_all()
        list_view = self.query_one("#todo_list_view", ListView)
        list_view.clear()
        for todo in self.todos:
            list_view.append(TodoItem(todo))

    def update_status(self, message: str) -> None:
        """Update status bar."""
        status_bar = self.query_one("#status_bar", Static)
        status_bar.update(f"▏ [dim]{message}[/]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "add_btn":
            self.add_todo()
        elif event.button.id == "complete_btn":
            self.complete_todo()
        elif event.button.id == "delete_btn":
            self.delete_todo()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle todo selection."""
        if event.item:
            self.selected_todo = event.item.todo
            self.update_status(f"Selected: {self.selected_todo.title}")

    def add_todo(self) -> None:
        """Add a new todo."""
        title_input = self.query_one("#title_input", Input)
        desc_input = self.query_one("#desc_input", Input)

        title = title_input.value.strip()
        if not title:
            self.update_status("[bold red]✗[/] Title required!")
            return

        description = desc_input.value.strip() or None
        todo = self.storage.create(title, description)

        title_input.value = ""
        desc_input.value = ""
        self.refresh_todos()
        self.update_status(f"[bold green]✓[/] Added: {todo.title}")

    def complete_todo(self) -> None:
        """Mark selected todo as complete."""
        if not self.selected_todo:
            self.update_status("[bold yellow]◉[/] Select a todo first")
            return

        if self.selected_todo.status == TodoStatus.DONE:
            self.update_status("[dim]◉[/] Already done")
            return

        self.storage.update(self.selected_todo.id, status=TodoStatus.DONE)
        self.refresh_todos()
        self.update_status(f"[bold green]✓[/] Completed: {self.selected_todo.title}")
        self.selected_todo = None

    def delete_todo(self) -> None:
        """Delete selected todo."""
        if not self.selected_todo:
            self.update_status("[bold yellow]◉[/] Select a todo first")
            return

        title = self.selected_todo.title
        self.storage.delete(self.selected_todo.id)
        self.refresh_todos()
        self.update_status(f"[bold red]✗[/] Deleted: {title}")
        self.selected_todo = None


def run_tui():
    """Run the TUI app."""
    app = TodoTui()
    app.run()
