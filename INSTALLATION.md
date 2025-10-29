# Installation and Distribution Guide

This document explains how to package and distribute `dyna-dialogs` for use in other applications.

## Package Structure

The package is now configured for installation via pip from a git repository:

```
dyna_dialogs/
├── core/              # Main package (always installed)
│   ├── __init__.py    # Exports: Dialog, create_dialog, TemplateParser, FieldFactory
│   ├── dialog.py      # Dialog manager
│   ├── parser.py      # Template parser
│   └── fields.py      # Field implementations
├── utils/             # Optional utilities (install with [logger] extra)
│   ├── __init__.py    # Exports: ProjectLogger
│   └── logger.py      # Logging utilities
├── examples/          # Not installed - for reference only
│   └── main.py        # Usage examples
├── pyproject.toml     # Package configuration
├── README.md          # User documentation
└── .gitignore         # Git exclusions
```

## Publishing to Git

### 1. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit - Dynamic Dialog System"
```

### 2. Create Remote Repository

Create a new repository on GitHub, GitLab, Bitbucket, etc. Then:

```bash
git remote add origin https://github.com/fikebr/dyna-dialogs.git
git push -u origin master
```

### 3. Tag Releases (Optional but Recommended)

```bash
# Tag current version
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# Users can then install specific versions:
# pip install git+https://github.com/fikebr/dyna-dialogs.git@v0.1.0
```

## Installation by Users

### Using pip

#### Basic Installation

```bash
# Install latest from default branch
pip install git+https://github.com/fikebr/dyna-dialogs.git

# Install with optional logger utilities
pip install "dyna-dialogs[logger] @ git+https://github.com/fikebr/dyna-dialogs.git"
```

#### Advanced pip Options

```bash
# Install specific version/tag
pip install git+https://github.com/fikebr/dyna-dialogs.git@v0.1.0

# Install from specific branch
pip install git+https://github.com/fikebr/dyna-dialogs.git@dev

# Install in editable mode (for development)
git clone https://github.com/fikebr/dyna-dialogs.git
cd dyna-dialogs
pip install -e .
pip install -e ".[logger]"  # with logger utilities
```

#### Using with requirements.txt

```txt
# requirements.txt
dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git

# Or specific version
dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git@v0.1.0

# With optional logger
dyna-dialogs[logger] @ git+https://github.com/fikebr/dyna-dialogs.git
```

### Using uv (Recommended)

If you use [uv](https://github.com/astral-sh/uv) for package management:

#### Add to Project

```bash
# From your project root, add dyna-dialogs as a dependency
uv add "dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git"

# With optional logger utilities
uv add "dyna-dialogs[logger] @ git+https://github.com/fikebr/dyna-dialogs.git"

# Add specific version
uv add "dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git@v0.1.0"
```

This automatically:
- Downloads and installs the package
- Adds it to your `pyproject.toml` dependencies
- Updates your `uv.lock` file

#### Manual Addition to pyproject.toml

Alternatively, edit your `pyproject.toml`:

```toml
[project]
dependencies = [
    "dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git",
    # your other dependencies...
]
```

Then sync:
```bash
uv sync
```

#### Update Package

```bash
# Update to latest from git
uv lock --upgrade-package dyna-dialogs

# Or remove and re-add
uv remove dyna-dialogs
uv add "dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git"
```

#### Editable Install for Development

```bash
# Clone the repository
git clone https://github.com/fikebr/dyna-dialogs.git
cd dyna-dialogs

# Install in editable mode
uv pip install -e .
uv pip install -e ".[logger]"  # with logger utilities
```

## Usage in Other Applications

### Import and Basic Usage

```python
from core import Dialog, create_dialog

# Simple dialog
template = """
User Settings|500x400
username|text
email|text
theme|selection|light,dark,auto
"""

result = create_dialog(template).show()
if result:
    print(f"Username: {result['username']}")
    print(f"Email: {result['email']}")
    print(f"Theme: {result['theme']}")
```

### With Custom Application Logging

If your application already has logging configured:

```python
import logging
from core import Dialog

# Use your existing logger
logger = logging.getLogger(__name__)

# The dialog will use your logging configuration
dialog = Dialog(template)
result = dialog.show()
```

### Using Optional Logger Utilities

If you installed with `[logger]` extra:

```python
from utils.logger import ProjectLogger
import logging

# Initialize once at application startup
ProjectLogger(keep=7, level=logging.DEBUG).init()

# Then use dialogs normally
from core import create_dialog
result = create_dialog(template).show()
```

## Updating the Package

### For Package Maintainers

1. Make changes to the code
2. Update version in `pyproject.toml`
3. Commit and push changes
4. Optionally create a new tag:
   ```bash
   git tag -a v0.2.0 -m "Release version 0.2.0"
   git push origin v0.2.0
   ```

### For Package Users

```bash
# Upgrade to latest version
pip install --upgrade git+https://github.com/fikebr/dyna-dialogs.git

# Or reinstall
pip uninstall dyna-dialogs
pip install git+https://github.com/fikebr/dyna-dialogs.git
```

## Migrating to PyPI (Optional Future Step)

If you later want to publish to PyPI for easier installation:

1. Build the package:
   ```bash
   pip install build twine
   python -m build
   ```

2. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

3. Users can then install with:
   ```bash
   pip install dyna-dialogs
   pip install dyna-dialogs[logger]
   ```

## Private Repository Notes

If your git repository is private:

1. Users need git credentials configured
2. For CI/CD, use SSH keys or deploy tokens
3. Installation format is the same:
   ```bash
   pip install git+ssh://git@github.com/fikebr/dyna-dialogs.git
   ```

## Troubleshooting

### "No module named 'tkinter'"

On Linux, install tkinter separately:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Import Errors After Installation

Make sure you're importing from the correct module:
```python
from core import Dialog, create_dialog  # Correct
# NOT: from dyna_dialogs.core import Dialog
```

### Git Installation Fails

- Ensure git is installed and in PATH
- Check repository URL is correct
- Verify you have access to the repository
- Try with SSH URL if HTTPS fails

