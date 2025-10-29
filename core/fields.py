"""Field handlers for different widget types."""

import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class BaseField:
    """Base class for all field types."""

    def __init__(self, parent: tk.Widget, name: str, options: List[str] = None):
        """Initialize the field."""
        self.parent = parent
        self.name = name
        self.options = options or []
        self.widget = None
        self.label = None

    def create(self) -> tk.Widget:
        """Create and return the widget container."""
        raise NotImplementedError("Subclasses must implement create()")

    def get_value(self) -> Any:
        """Extract and return the current value of the field."""
        raise NotImplementedError("Subclasses must implement get_value()")

    def set_value(self, value: Any):
        """Set the value of the field."""
        raise NotImplementedError("Subclasses must implement set_value()")


class TextField(BaseField):
    """Single-line text entry field."""

    def create(self) -> tk.Widget:
        """Create text entry with label."""
        container = tk.Frame(self.parent)
        
        # Create label
        self.label = tk.Label(container, text=self.name, anchor='w')
        self.label.pack(side=tk.TOP, fill=tk.X, pady=(0, 2))
        
        # Create entry
        self.widget = tk.Entry(container)
        self.widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        logger.debug(f"Created text field: {self.name}")
        return container

    def get_value(self) -> str:
        """Return the text value."""
        return self.widget.get()

    def set_value(self, value: str):
        """Set the text value."""
        self.widget.delete(0, tk.END)
        self.widget.insert(0, str(value))
        logger.debug(f"Set text field '{self.name}' to: {value}")


class MultilineField(BaseField):
    """Multi-line text area field."""

    def create(self) -> tk.Widget:
        """Create text area with scrollbar and label."""
        container = tk.Frame(self.parent)
        
        # Create label
        self.label = tk.Label(container, text=self.name, anchor='w')
        self.label.pack(side=tk.TOP, fill=tk.X, pady=(0, 2))
        
        # Create frame for text and scrollbar
        text_frame = tk.Frame(container)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget
        self.widget = tk.Text(text_frame, height=5, yscrollcommand=scrollbar.set)
        self.widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.widget.yview)
        
        logger.debug(f"Created multiline field: {self.name}")
        return container

    def get_value(self) -> str:
        """Return the text content."""
        return self.widget.get('1.0', 'end-1c')

    def set_value(self, value: str):
        """Set the text content."""
        self.widget.delete('1.0', tk.END)
        self.widget.insert('1.0', str(value))
        logger.debug(f"Set multiline field '{self.name}' to: {value}")


class SelectionField(BaseField):
    """Dropdown selection field."""

    def create(self) -> tk.Widget:
        """Create combobox with label."""
        container = tk.Frame(self.parent)
        
        # Create label
        self.label = tk.Label(container, text=self.name, anchor='w')
        self.label.pack(side=tk.TOP, fill=tk.X, pady=(0, 2))
        
        # Create combobox
        self.widget = ttk.Combobox(container, values=self.options, state='readonly')
        if self.options:
            self.widget.current(0)  # Select first option by default
        self.widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        logger.debug(f"Created selection field: {self.name} with options: {self.options}")
        return container

    def get_value(self) -> str:
        """Return the selected value."""
        return self.widget.get()

    def set_value(self, value: str):
        """Set the selected value."""
        value_str = str(value).strip()
        if value_str in self.options:
            self.widget.set(value_str)
            logger.debug(f"Set selection field '{self.name}' to: {value_str}")
        else:
            logger.warning(f"Value '{value_str}' not in options for field '{self.name}': {self.options}")


class CheckgroupField(BaseField):
    """Multiple checkbox group field."""

    def __init__(self, parent: tk.Widget, name: str, options: List[str] = None):
        """Initialize checkgroup field."""
        super().__init__(parent, name, options)
        self.check_vars = []

    def create(self) -> tk.Widget:
        """Create checkbox group with label."""
        container = tk.Frame(self.parent)
        
        # Create label
        self.label = tk.Label(container, text=self.name, anchor='w')
        self.label.pack(side=tk.TOP, fill=tk.X, pady=(0, 2))
        
        # Create checkboxes
        self.check_vars = []
        for option in self.options:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(container, text=option, variable=var)
            cb.pack(side=tk.TOP, anchor='w', padx=(20, 0))
            self.check_vars.append((option, var))
        
        logger.debug(f"Created checkgroup field: {self.name} with {len(self.options)} options")
        return container

    def get_value(self) -> List[str]:
        """Return list of checked options."""
        return [option for option, var in self.check_vars if var.get()]

    def set_value(self, value):
        """Set checked options from comma-delimited string or list."""
        if isinstance(value, str):
            # Split by comma and strip whitespace
            values = [v.strip() for v in value.split(',') if v.strip()]
        elif isinstance(value, list):
            values = [str(v).strip() for v in value]
        else:
            values = [str(value).strip()]
        
        # Update checkbox states
        for option, var in self.check_vars:
            var.set(option in values)
        
        logger.debug(f"Set checkgroup field '{self.name}' to: {values}")


class RadioField(BaseField):
    """Radio button group field."""

    def __init__(self, parent: tk.Widget, name: str, options: List[str] = None):
        """Initialize radio field."""
        super().__init__(parent, name, options)
        self.radio_var = tk.StringVar()

    def create(self) -> tk.Widget:
        """Create radio button group with label."""
        container = tk.Frame(self.parent)
        
        # Create label
        self.label = tk.Label(container, text=self.name, anchor='w')
        self.label.pack(side=tk.TOP, fill=tk.X, pady=(0, 2))
        
        # Create radio buttons
        if self.options:
            self.radio_var.set(self.options[0])  # Select first by default
        
        for option in self.options:
            rb = tk.Radiobutton(container, text=option, variable=self.radio_var, value=option)
            rb.pack(side=tk.TOP, anchor='w', padx=(20, 0))
        
        logger.debug(f"Created radio field: {self.name} with {len(self.options)} options")
        return container

    def get_value(self) -> str:
        """Return the selected radio option."""
        return self.radio_var.get()

    def set_value(self, value: str):
        """Set the selected radio option."""
        value_str = str(value).strip()
        if value_str in self.options:
            self.radio_var.set(value_str)
            logger.debug(f"Set radio field '{self.name}' to: {value_str}")
        else:
            logger.warning(f"Value '{value_str}' not in options for field '{self.name}': {self.options}")


class ButtonField(BaseField):
    """Custom button field."""

    def __init__(self, parent: tk.Widget, name: str, options: List[str] = None, 
                 callback: Optional[Callable] = None):
        """Initialize button field."""
        super().__init__(parent, name, options)
        self.callback = callback

    def create(self) -> tk.Widget:
        """Create button (no label for buttons)."""
        container = tk.Frame(self.parent)
        
        # Create button
        self.widget = tk.Button(container, text=self.name, command=self._on_click)
        self.widget.pack(side=tk.TOP, pady=5)
        
        logger.debug(f"Created button field: {self.name}")
        return container

    def _on_click(self):
        """Handle button click."""
        if self.callback:
            self.callback()
        else:
            logger.warning(f"No callback set for button: {self.name}")

    def get_value(self) -> None:
        """Buttons don't have a value."""
        return None

    def set_value(self, value):
        """Buttons don't have a value to set."""
        logger.debug(f"Ignoring set_value for button: {self.name}")


class DividerField(BaseField):
    """Horizontal divider line."""

    def create(self) -> tk.Widget:
        """Create divider (no label)."""
        container = tk.Frame(self.parent, height=20)
        
        # Create separator
        separator = ttk.Separator(container, orient='horizontal')
        separator.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        logger.debug("Created divider field")
        return container

    def get_value(self) -> None:
        """Dividers don't have a value."""
        return None

    def set_value(self, value):
        """Dividers don't have a value to set."""
        pass


class FieldFactory:
    """Factory for creating field instances."""

    _field_types = {
        'text': TextField,
        'multiline': MultilineField,
        'selection': SelectionField,
        'checkgroup': CheckgroupField,
        'radio': RadioField,
        'button': ButtonField,
        'divider': DividerField
    }

    @classmethod
    def create_field(cls, parent: tk.Widget, field_data: Dict, 
                     callback: Optional[Callable] = None) -> BaseField:
        """Create a field instance based on field data."""
        field_type = field_data['type']
        field_name = field_data['name']
        options = field_data.get('options', [])

        if field_type not in cls._field_types:
            raise ValueError(f"Unknown field type: {field_type}")

        field_class = cls._field_types[field_type]
        
        # Button fields need callback
        if field_type == 'button':
            return field_class(parent, field_name, options, callback)
        else:
            return field_class(parent, field_name, options)

