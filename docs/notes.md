# dynamic tk dialogs

create a TK dialog based on a simple text template.

the dialog is represented in a class object. when a button type is clicked the object is passed to the function call 

## Status: IMPLEMENTED ✓

All features have been implemented in the core/ directory.

## dialog template

```
title|HxW
field|type|options
```

Example:
```
User Settings|500x400
username|text
theme|selection|light,dark,auto
```

## field types

- **text** - Single-line text entry with label
- **multiline** - Multi-line text area with scrollbar and label
- **selection** - Dropdown combobox with label
- **checkgroup** - Multiple checkboxes with label
- **radio** - Radio button group with label
- **button** - Custom button (no label, triggers callback specified in template)
- **divider** - Horizontal separator (no label)

## Usage

```python
from core import Dialog

# Define callback functions
def my_callback(dialog):
    print("Button clicked!")
    print(dialog.values)

# Create dialog with inline callbacks
template = """
Settings|400x300
username|text
reset|button|main.my_callback
"""

dialog = Dialog(template)

# Show dialog (returns dict or None)
result = dialog.show()
```

## Button Callbacks

Button fields can specify their callback function inline:
- Format: `button_name|button|module.function` (e.g., `reset|button|main.reset_callback`)
- Or use bare function name: `button_name|button|function_name` (searches in `__main__` module)
- The callback receives the Dialog object as a parameter, allowing access to `dialog.values`

## Files

- `core/parser.py` - Template parser
- `core/fields.py` - Field type handlers
- `core/dialog.py` - Dialog manager
- `core/__init__.py` - Public API
- `main.py` - Examples
