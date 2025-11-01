# Contributing to dyna-dialogs

Thank you for your interest in contributing to dyna-dialogs!

## Development Workflow

If you're using dyna-dialogs in your project and want to contribute improvements back, follow this workflow:

### Setup for Development

1. **Clone the repository**:
   ```bash
   cd ~/projects  # or your preferred location
   git clone https://github.com/fikebr/dyna-dialogs.git
   cd dyna-dialogs
   ```

2. **Install in editable mode** in your project:
   ```bash
   cd ~/projects/your-project
   
   # Using uv
   uv pip install -e ~/projects/dyna-dialogs
   
   # Using pip
   pip install -e ~/projects/dyna-dialogs
   ```

   With editable mode, changes to dyna-dialogs are immediately reflected in your project.

3. **Create a feature branch**:
   ```bash
   cd ~/projects/dyna-dialogs
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. **Edit the code** in `~/projects/dyna-dialogs/`:
   - Core functionality: `core/dialog.py`, `core/fields.py`, `core/parser.py`
   - Utilities: `utils/logger.py`
   - Documentation: `README.md`, `INSTALLATION.md`, etc.

2. **Test your changes** in your project:
   ```bash
   cd ~/projects/your-project
   python your_script.py  # Uses your edited dyna-dialogs
   ```

3. **Test with the examples**:
   ```bash
   cd ~/projects/dyna-dialogs
   python main.py  # Run the development examples
   ```

### Committing Changes

1. **Review your changes**:
   ```bash
   cd ~/projects/dyna-dialogs
   git status
   git diff
   ```

2. **Commit with clear messages**:
   ```bash
   git add <changed_files>
   git commit -m "Brief description of changes"
   ```

   Good commit messages:
   - ✅ "Add validation for empty field names in parser"
   - ✅ "Fix: Handle None values in set_field_value"
   - ✅ "Docs: Update README with new field type"
   - ❌ "Fixed stuff"
   - ❌ "WIP"

3. **Push to your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting Changes

1. **Create a Pull Request** on GitHub
   - Describe what changes you made and why
   - Reference any related issues
   - Include examples if adding new features

2. **Wait for review**
   - Address any feedback
   - Make additional commits if needed

3. **After merge**:
   ```bash
   # Update your local master
   git checkout master
   git pull origin master
   
   # Delete feature branch
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

## Switching Between Development and Production

### During Development
Use editable install:
```bash
uv pip install -e ~/projects/dyna-dialogs
```

### For Production
Switch back to git URL:
```bash
uv remove dyna-dialogs
uv add "dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git"
```

### Quick Toggle Script
```bash
# dev-mode.sh
cd ~/projects/your-project
uv pip uninstall dyna-dialogs -y
uv pip install -e ~/projects/dyna-dialogs
echo "Switched to development mode"

# prod-mode.sh
cd ~/projects/your-project
uv remove dyna-dialogs
uv add "dyna-dialogs @ git+https://github.com/fikebr/dyna-dialogs.git"
echo "Switched to production mode"
```

## Code Guidelines

### Python Style
- Follow PEP 8 conventions
- Use type hints where applicable
- Keep docstrings simple (single sentence describing function)
- Maximum line length: 100 characters

### Logging
- Use the existing logger: `logger = logging.getLogger(__name__)`
- Log levels:
  - `DEBUG`: Detailed information for debugging
  - `INFO`: Confirmation of expected behavior
  - `WARNING`: Something unexpected but handled
  - `ERROR`: Serious problem with exception info

### Error Handling
- Use try/except blocks for operations that can fail
- Log errors with `logger.error()` and `exc_info=True`
- Return sensible defaults or None rather than raising

### Testing
- Test your changes with the examples in `main.py`
- Ensure existing functionality still works
- Test edge cases (empty strings, None values, etc.)

## Project Structure

```
dyna_dialogs/
├── core/               # Main package
│   ├── __init__.py    # Public API exports
│   ├── dialog.py      # Dialog manager and display
│   ├── parser.py      # Template parsing logic
│   └── fields.py      # Field type implementations
├── utils/             # Utilities
│   ├── __init__.py    # Utility exports
│   └── logger.py      # Logging utilities
├── examples/          # Usage examples
│   └── main.py        # Example scripts
├── docs/              # Additional documentation
├── main.py            # Development test file
└── README.md          # Main documentation
```

## Adding New Features

### New Field Type
1. Add field class to `core/fields.py` (inherit from `BaseField`)
2. Implement `create()`, `get_value()`, `set_value()` methods
3. Register in `FieldFactory._field_types` dictionary
4. Add to valid types in `core/parser.py`
5. Document in `README.md` field types table
6. Add example to `examples/main.py`

### New Dialog Feature
1. Update `core/dialog.py` with new functionality
2. Update public API in `core/__init__.py` if needed
3. Add documentation and examples

## Questions or Issues?

- Open an issue on GitHub for bugs or feature requests
- Check existing issues before creating new ones
- Include minimal reproduction example for bugs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉

