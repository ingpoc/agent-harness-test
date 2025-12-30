# ◆ CLI Todo App

A distinctive terminal todo manager with intentional aesthetics.

## Aesthetic: Minimalist Zen

- Palette: Nord-inspired cool blues on dark gray
- Borders: Rounded (╭─╮│╰╯)
- Status symbols: ▸ pending, ✓ done, ○ empty

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run CLI
python -m todo_cli.cli --help
```

## Usage

```bash
# Add a todo
python -m todo_cli.cli add "Fix authentication" --desc "Add JWT tokens"

# List all todos
python -m todo_cli.cli list

# Complete a todo
python -m todo_cli.cli complete F-001

# Delete a todo
python -m todo_cli.cli delete F-001
```

## Features

- ✅ Add todos with titles and descriptions
- ✅ List todos with styled table output
- ✅ Mark todos as complete
- ✅ Delete todos
- 🔜 Data persistence (JSON storage)
- 🔜 Filter by status

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=todo_cli
```

## Design Philosophy

This CLI demonstrates the **terminal-ui-design** skill principles:
- Intentional aesthetic (not generic)
- Cohesive color palette
- Unicode borders and symbols
- Anti-patterns avoided (no plain text, styled output)
