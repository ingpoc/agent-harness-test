# CLI Todo App with Terminal UI

A beautiful terminal-based todo application with both CLI commands and an interactive TUI.

## Features

- Add, list, complete, and delete todos
- Interactive Terminal UI with rich styling
- Color-coded status (pending=yellow, done=green)
- Persistent JSON storage

## Installation

\`\`\`bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install -e .
\`\`\`

## Usage

### CLI Commands
\`\`\`bash
# Add a todo
todo add "Buy groceries" --description "Milk, eggs, bread"

# List all todos
todo list

# List only pending
todo list --status pending

# Complete a todo
todo complete 1

# Delete a todo
todo delete 1
\`\`\`

### Interactive TUI
\`\`\`bash
# Launch interactive terminal UI
todo tui
\`\`\`

## Development

\`\`\`bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/todo_cli
\`\`\`
