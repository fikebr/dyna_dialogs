# Quick Start Guide for Developers

This guide shows how to quickly integrate `dyna-dialogs` into your Python applications.

## Installation

```bash
pip install git+https://github.com/fikebr/dyna-dialogs.git
```

## Basic Usage

### 1. Simple Text Input Dialog

```python
from core import create_dialog

template = """
Enter Details|400x200
name|text
age|text
"""

result = create_dialog(template).show()
if result:
    print(f"Name: {result['name']}, Age: {result['age']}")
```

### 2. Configuration Dialog

```python
from core import Dialog

template = """
App Settings|500x400
api_key|text
environment|selection|development,staging,production
debug_mode|checkgroup|Enable Debug Logging
"""

dialog = Dialog(template)
config = dialog.show()

if config:
    # Use the configuration in your app
    API_KEY = config['api_key']
    ENV = config['environment']
    DEBUG = 'Enable Debug Logging' in config['debug_mode']
```

### 3. With Custom Buttons

```python
from core import Dialog

def validate_and_save(dialog):
    """Custom validation before saving."""
    values = dialog.values
    if not values.get('email'):
        print("Email is required!")
        return
    
    # Save logic here
    print(f"Saving: {values}")

template = """
User Form|450x400
name|text
email|text
role|radio|admin,user,guest
validate|button|__main__.validate_and_save
|divider
"""

dialog = Dialog(template)
result = dialog.show()
```

### 4. Loading from File

```python
from core import create_dialog
from pathlib import Path

# Save template to file
template_file = Path("my_dialog.txt")
template_file.write_text("""
Database Config|500x300
host|text
port|text
database|text
""")

# Load and show
result = create_dialog(template_file).show()
```

### 5. Dynamic Field Values

```python
from core import Dialog

template = """
Edit Profile|500x450
username|text
email|text
bio|multiline
theme|selection|light,dark,auto
"""

dialog = Dialog(template)

# Pre-populate with existing values
dialog.set_field_value('username', 'john_doe')
dialog.set_field_value('email', 'john@example.com')
dialog.set_field_value('bio', 'Software developer')
dialog.set_field_value('theme', 'dark')

# Show and get updated values
result = dialog.show()
```

## Template Format Reference

### Header
```
Title|WidthxHeight
```

### Field Types

| Type | Example | Returns |
|------|---------|---------|
| `text` | `username\|text` | String |
| `multiline` | `description\|multiline` | String |
| `selection` | `theme\|selection\|opt1,opt2,opt3` | String |
| `checkgroup` | `features\|checkgroup\|opt1,opt2,opt3` | List[str] |
| `radio` | `role\|radio\|opt1,opt2,opt3` | String |
| `button` | `save\|button\|module.function` | None |
| `divider` | `\|divider` | None |

## Complete Example Application

```python
#!/usr/bin/env python3
"""Example application using dyna-dialogs."""

import logging
from core import Dialog

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def export_config(dialog):
    """Export current configuration to file."""
    config = dialog.values
    logger.info(f"Exporting config: {config}")
    # Export logic here

def reset_defaults(dialog):
    """Reset all fields to defaults."""
    dialog.set_field_value('server', 'localhost')
    dialog.set_field_value('port', '5432')
    dialog.set_field_value('ssl', 'enabled')
    logger.info("Reset to defaults")

def main():
    template = """
Database Connection|550x500
server|text
port|text
database|text
username|text
password|text
ssl|radio|enabled,disabled
options|checkgroup|Auto-connect,Pool connections,Use compression
export|button|__main__.export_config
reset|button|__main__.reset_defaults
|divider
"""
    
    dialog = Dialog(template)
    
    # Set defaults
    dialog.set_field_value('server', 'localhost')
    dialog.set_field_value('port', '5432')
    dialog.set_field_value('ssl', 'enabled')
    dialog.set_field_value('options', ['Auto-connect', 'Pool connections'])
    
    # Show dialog
    result = dialog.show()
    
    if result:
        logger.info("Connection configuration:")
        for key, value in result.items():
            logger.info(f"  {key}: {value}")
        
        # Connect using the configuration
        # connect_to_database(result)
    else:
        logger.info("Configuration cancelled")

if __name__ == '__main__':
    main()
```

## Integration Patterns

### Pattern 1: Configuration Wizard

```python
def get_app_config():
    """Get application configuration from user."""
    template = """
Application Setup|600x500
app_name|text
api_endpoint|text
auth_type|selection|api_key,oauth,basic
log_level|radio|DEBUG,INFO,WARNING,ERROR
features|checkgroup|Analytics,Caching,Auto-updates
"""
    return create_dialog(template).show()

config = get_app_config()
if config:
    initialize_app(config)
```

### Pattern 2: Input Validation

```python
def get_user_input():
    """Get and validate user input."""
    while True:
        result = create_dialog(template).show()
        
        if not result:  # User cancelled
            return None
        
        # Validate
        if result['email'] and '@' in result['email']:
            return result
        
        print("Invalid email! Please try again.")
```

### Pattern 3: Settings Editor

```python
class AppSettings:
    def __init__(self):
        self.settings = self.load_settings()
    
    def edit(self):
        """Show settings dialog with current values."""
        dialog = Dialog(self.template)
        
        # Load current settings
        for key, value in self.settings.items():
            dialog.set_field_value(key, value)
        
        # Get updates
        result = dialog.show()
        if result:
            self.settings.update(result)
            self.save_settings()
        
        return result
```

## Tips

1. **Field Names**: Use descriptive names - they become dictionary keys
2. **Callbacks**: Must be callable and accept dialog as parameter
3. **Values**: Access current values anytime with `dialog.values`
4. **Pre-population**: Use `set_field_value()` before `show()`
5. **Validation**: Implement in custom button callbacks
6. **Multi-step**: Chain multiple dialogs for wizards

## Next Steps

- See `examples/main.py` for more examples
- Read `README.md` for complete field type documentation
- Check `INSTALLATION.md` for deployment details

