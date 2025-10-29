# Packaging Notes

## Before Publishing

### 1. Update Author Information

Edit `pyproject.toml` and replace the placeholder author information:

```toml
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
```

### 2. Update Repository URLs

✅ Repository URLs have been updated to use GitHub username: **fikebr**

Updated in:
- `pyproject.toml` - Homepage, Repository, Issues URLs
- `README.md` - Installation instructions
- `INSTALLATION.md` - All example URLs
- `examples/main.py` - Installation documentation

### 3. Create Git Repository

```bash
# Initialize if not already done
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Dynamic Dialog System"

# Add remote
git remote add origin https://github.com/fikebr/dyna-dialogs.git

# Push to remote
git push -u origin master
```

### 4. Create Initial Release Tag

```bash
git tag -a v0.1.0 -m "Initial release - v0.1.0"
git push origin v0.1.0
```

## Package Configuration

The package is configured in `pyproject.toml`:

- **Build System**: Uses `hatchling` (lightweight, modern)
- **Packages**: Includes `core` and `utils`
- **Optional Dependencies**: `logger` extra for utilities
- **Python Version**: Requires >= 3.12

## Distribution Methods

### Method 1: Git Repository (Current)

**Advantages:**
- No additional accounts needed
- Private repository support
- Easy updates (just push)
- Version control via git tags

**Installation:**
```bash
pip install git+https://github.com/yourusername/dyna-dialogs.git
```

### Method 2: PyPI (Future Option)

**Advantages:**
- Simple `pip install dyna-dialogs`
- More discoverable
- Official Python package repository

**Setup Required:**
1. Create PyPI account at https://pypi.org
2. Install build tools: `pip install build twine`
3. Build: `python -m build`
4. Upload: `twine upload dist/*`

## Testing Installation

Before distributing, test the installation process:

### Local Testing

```bash
# Create test virtual environment
python -m venv test_env
source test_env/bin/activate  # or test_env\Scripts\activate on Windows

# Install from local directory
pip install .

# Test basic import
python -c "from core import Dialog, create_dialog; print('Success!')"

# Test with logger extra
pip install ".[logger]"
python -c "from utils.logger import ProjectLogger; print('Logger available!')"
```

### Git Installation Testing

After pushing to git:

```bash
# New virtual environment
python -m venv test_git_env
source test_git_env/bin/activate

# Install from git
pip install git+https://github.com/yourusername/dyna-dialogs.git

# Test
python -c "from core import create_dialog; print('Git install successful!')"
```

## What Gets Installed

When users install the package, they get:

**Always Installed:**
- `core/` - All dialog functionality
- `utils/` - Logger utilities (always available)

**Not Installed:**
- `examples/` - Example scripts
- `docs/` - Documentation
- `main.py` - Development test file
- `log/` - Log files
- Build artifacts

## Version Management

### Semantic Versioning

Use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes (1.0.0 → 2.0.0)
- **MINOR**: New features, backwards compatible (1.0.0 → 1.1.0)
- **PATCH**: Bug fixes (1.0.0 → 1.0.1)

### Updating Version

1. Edit `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Commit and tag:
   ```bash
   git commit -am "Bump version to 0.2.0"
   git tag -a v0.2.0 -m "Version 0.2.0 - New features"
   git push origin master
   git push origin v0.2.0
   ```

## Dependencies

Currently uses **zero external dependencies** - only Python standard library:
- `tkinter` - GUI (must be installed separately on some Linux systems)
- `logging` - Logging
- `pathlib` - Path handling

If you add dependencies in the future, update `pyproject.toml`:

```toml
dependencies = [
    "requests>=2.28.0",
    "pyyaml>=6.0",
]
```

## Private Repository Distribution

For private/internal packages:

### SSH Installation
```bash
pip install git+ssh://git@github.com/yourusername/dyna-dialogs.git
```

### With Authentication Token
```bash
pip install git+https://TOKEN@github.com/yourusername/dyna-dialogs.git
```

### In requirements.txt
```txt
dyna-dialogs @ git+ssh://git@github.com/yourusername/dyna-dialogs.git@v0.1.0
```

## Maintenance Checklist

### Before Each Release

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` (if you create one)
- [ ] Run tests (if you add them)
- [ ] Test installation locally
- [ ] Commit all changes
- [ ] Create git tag
- [ ] Push to remote

### Regular Maintenance

- [ ] Review and respond to issues
- [ ] Keep dependencies updated (if any)
- [ ] Maintain backwards compatibility
- [ ] Document breaking changes
- [ ] Update examples as needed

## Documentation Files

Your package now includes:

1. **README.md** - User-facing documentation
2. **INSTALLATION.md** - Detailed installation guide
3. **QUICK_START.md** - Quick reference for developers
4. **PACKAGING_NOTES.md** - This file (maintainer notes)

Consider adding:
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - License file (MIT recommended)

## Next Steps

1. Replace placeholder information (author, URLs)
2. Push to git repository
3. Create initial release tag
4. Share repository URL with users
5. Consider adding to PyPI when stable

