# Dynamic Dialog System

Create tkinter dialogs from simple pipe-delimited text templates.

## Features

- **Simple Template Format**: Define dialogs using intuitive pipe-delimited syntax
- **7 Field Types**: text, multiline, selection, checkgroup, radio, button, divider
- **Auto OK/Cancel**: Automatically adds OK (returns dict) and Cancel (returns None) buttons
- **Custom Buttons**: Add custom buttons with callback functions
- **File or String**: Load templates from files or inline strings
- **Optional Logging**: Include optional logger utilities for comprehensive logging
- **Error Handling**: Graceful error handling for malformed templates
- **Pure Python**: Uses only Python standard library (tkinter, logging, pathlib)

## Installation

### Using pip

```bash
# Basic installation (core functionality only)
pip install git+https://github.com/fikebr/dyna-dialogs.git

# With optional logger utilities
pip install "dyna-dialogs[logger] @ git+https://github.com/fikebr/dyna-dialogs.git"

# Install specific tag/version
pip install git+https://github.com/fikebr/dyna-dialogs.git@v1.0.0

# Install from specific branch
pip install git+https://github.com/fikebr/dyna-dialogs.git@dev

# Editable mode for development
git clone https://github.com/fikebr/dyna-dialogs.git
cd dyna-dialogs
pip install -e .
pip install -e ".[logger]"  # with logger utilities
```

### Using uv (Recommended)

If you use [uv](https://github.com/astral-sh/uv) for package management:

```bash
# Add as dependency to your project
uv add "dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git"

# Add with optional logger utilities
uv add "dyna-dialogs[logger] @ git+https://github.com/fikebr/dyna-dialogs.git"

# Add specific version
uv add "dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git@v0.1.0"

# Or manually add to pyproject.toml dependencies, then:
uv sync
```

This adds dyna-dialogs to your `pyproject.toml` and `uv.lock` automatically.

### Requirements

- Python >= 3.12
- tkinter (included with most Python installations)

**Note for Linux users:** If tkinter is not available, install it with:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Quick Start

### Simple Example

```python
from core import create_dialog

template = """
Contact Form|450x350
name|text
email|text
message|multiline
"""

result = create_dialog(template).show()

if result:
    print(f"Name: {result['name']}")
    print(f"Email: {result['email']}")
    print(f"Message: {result['message']}")
else:
    print("Cancelled")
```

### With Custom Buttons

```python
from core import Dialog

def reset_callback(dialog):
    print(f"Current values: {dialog.values}")

template = """
Settings|500x400
username|text
theme|selection|light,dark,auto
reset|button|__main__.reset_callback
"""

dialog = Dialog(template)
result = dialog.show()
```

## Template Format

### Header Line
```
Title|WidthxHeight
```

Example: `User Settings|500x400`

### Field Lines
```
field_name|field_type|options
```

## Field Types

| Type | Description | Options Format | Returns |
|------|-------------|----------------|---------|
| `text` | Single-line text input | - | String |
| `multiline` | Multi-line text area | - | String |
| `selection` | Dropdown menu | `opt1,opt2,opt3` | String |
| `checkgroup` | Multiple checkboxes | `opt1,opt2,opt3` | List of strings |
| `radio` | Radio button group | `opt1,opt2,opt3` | String |
| `button` | Custom button | `module.function` or `function` | None (triggers callback) |
| `divider` | Horizontal line | - | None |

## Complete Example

```python
from core import Dialog

def save_settings(dialog):
    values = dialog.values
    print(f"Saving: {values}")

template = """
User Preferences|550x500
username|text
bio|multiline
theme|selection|light,dark,auto
notifications|checkgroup|email,sms,push
role|radio|admin,user,guest
save|button|main.save_settings
|divider
"""

dialog = Dialog(template)
result = dialog.show()

if result:
    print("Settings saved:", result)
else:
    print("Cancelled")
```

## Button Callbacks

Button fields specify their callback function inline:
- **Module format**: `button_name|button|module.function` (e.g., `save|button|main.save_settings`)
- **Bare function**: `button_name|button|function_name` (searches in `__main__` module)
- Callbacks receive the Dialog object as parameter, allowing access to `dialog.values`

## Using in Your Application

After installation, import and use the dialogs in your application:

```python
from core import Dialog, create_dialog

# Simple usage
result = create_dialog("Title|400x300\nfield1|text").show()

# Advanced usage
dialog = Dialog(template_string_or_file_path)
result = dialog.show()
```

## Running Examples

The `examples/` directory contains usage examples:

```bash
# Clone the repository first
git clone https://github.com/fikebr/dyna-dialogs.git
cd dyna-dialogs

# Run examples (requires optional logger utilities)
python examples/main.py
```

## Project Structure

```
dyna_dialogs/
├── core/              # Main package (always installed)
│   ├── __init__.py    # Public API: Dialog, create_dialog
│   ├── parser.py      # Template parser
│   ├── fields.py      # Field type handlers
│   └── dialog.py      # Dialog manager
├── utils/             # Optional utilities (logger extra)
│   └── logger.py      # Logging utilities
├── examples/          # Example scripts (not installed)
│   └── main.py        # Usage examples
├── pyproject.toml     # Package configuration
└── README.md
```

## Optional: Logging Utilities

If you installed with the `[logger]` extra, you can use the included `ProjectLogger`:

```python
from utils.logger import ProjectLogger
import logging

# Initialize once at startup
ProjectLogger(keep=7, level=logging.DEBUG).init()
logger = logging.getLogger(__name__)
```

Features:
- Logs stored in `log/YYYY-MM-DD.log` with daily rotation
- Keeps 7 most recent log files
- Debug-level logging (configurable)
- Compact format: `HHMMSS - ERR|WRN|INF|DBG - file - function:line - message`
- Error tracking with stack traces

**Note:** The core dialog functionality works with or without this logger. It uses standard Python logging, so you can use any logging configuration you prefer.

## License

MIT

