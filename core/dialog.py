"""Dialog manager for creating and displaying dialogs."""

import importlib
import logging
import sys
import tkinter as tk
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

from core.fields import FieldFactory
from core.parser import TemplateParser

logger = logging.getLogger(__name__)


class Dialog:
    """Main dialog class for creating and managing dialogs."""

    def __init__(self, template: Union[str, Path]):
        """Initialize dialog with a template."""
        self.template = template
        self.root = None
        self.fields = []
        self.result = None
        self.first_focusable_widget = None
        
        # Parse template
        try:
            parser = TemplateParser(template)
            self.config = parser.parse()
            logger.info(f"Parsed template: {self.config['title']}")
        except Exception as e:
            logger.error(f"Failed to parse template: {e}")
            raise

    @property
    def values(self) -> Dict[str, Any]:
        """Get current values from all fields."""
        values = {}
        for field in self.fields:
            value = field.get_value()
            # Only include fields that have values (exclude buttons, dividers)
            if value is not None:
                values[field.name] = value
        return values

    def set_field_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a field by name."""
        for field in self.fields:
            if field.name == field_name:
                try:
                    field.set_value(value)
                    logger.debug(f"Set field '{field_name}' to value: {value}")
                    return True
                except Exception as e:
                    logger.error(f"Error setting field '{field_name}': {e}")
                    return False
        logger.warning(f"Field '{field_name}' not found in dialog")
        return False

    def show(self) -> Optional[Dict[str, Any]]:
        """Display the dialog and return the result."""
        self.result = None
        
        # Create root window
        self.root = tk.Tk()
        self.root.title(self.config['title'])
        
        # Set size if specified
        if self.config['size']:
            width, height = self.config['size']
            self.root.geometry(f"{width}x{height}")
            logger.debug(f"Set window size: {width}x{height}")
        
        # Create main frame with padding
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable content area
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Make scrollable_frame expand with canvas width
        def _on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        # Build fields
        self._build_fields(scrollable_frame)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create button frame at bottom
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add OK and Cancel buttons
        ok_btn = tk.Button(button_frame, text="OK", command=self._on_ok, width=10)
        ok_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self._on_cancel, width=10)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Bind keyboard shortcuts
        self.root.bind("<Escape>", lambda event: self._on_cancel())
        self.root.bind("<Control-Return>", lambda event: self._on_ok())
        logger.debug("Bound keyboard shortcuts: Escape for Cancel, Ctrl+Enter for OK")
        
        # Center window on screen
        self.root.update_idletasks()
        self._center_window()
        
        # Make dialog modal
        self.root.grab_set()
        
        # Focus on first field if available
        if self.first_focusable_widget:
            self.first_focusable_widget.focus_set()
            logger.debug("Set focus to first field")
        else:
            self.root.focus_force()
        
        logger.info(f"Showing dialog: {self.config['title']}")
        
        # Start main loop
        self.root.mainloop()
        
        return self.result

    def _resolve_callback(self, callback_str: str) -> Optional[Callable]:
        """Resolve a callback string to an actual callable function."""
        if not callback_str:
            return None
            
        try:
            # Check if callback string contains a dot (module.function format)
            if '.' in callback_str:
                parts = callback_str.rsplit('.', 1)
                module_name = parts[0]
                function_name = parts[1]
                
                try:
                    # Try to import the module
                    module = importlib.import_module(module_name)
                    callback = getattr(module, function_name, None)
                    
                    if callback and callable(callback):
                        logger.debug(f"Resolved callback: {callback_str}")
                        return callback
                    else:
                        logger.warning(f"Callback '{callback_str}' not found or not callable")
                        return None
                        
                except (ImportError, AttributeError) as e:
                    logger.warning(f"Failed to import callback '{callback_str}': {e}")
                    return None
            else:
                # No dot, search in __main__ module namespace
                main_module = sys.modules.get('__main__')
                if main_module:
                    callback = getattr(main_module, callback_str, None)
                    
                    if callback and callable(callback):
                        logger.debug(f"Resolved callback from __main__: {callback_str}")
                        return callback
                    else:
                        logger.warning(f"Callback '{callback_str}' not found in __main__ module")
                        return None
                else:
                    logger.warning(f"__main__ module not available, cannot resolve '{callback_str}'")
                    return None
                    
        except Exception as e:
            logger.error(f"Error resolving callback '{callback_str}': {e}")
            return None

    def _build_fields(self, parent: tk.Widget):
        """Build all fields from the configuration."""
        for field_data in self.config['fields']:
            try:
                # For button fields, resolve the callback
                if field_data['type'] == 'button':
                    callback_str = field_data.get('callback')
                    callback = None
                    
                    if callback_str:
                        resolved_callback = self._resolve_callback(callback_str)
                        if resolved_callback:
                            # Wrap callback to pass dialog object
                            def callback(dialog_ref=self, cb=resolved_callback):
                                try:
                                    cb(dialog_ref)
                                    logger.debug(f"Executed callback: {callback_str}")
                                except Exception as e:
                                    logger.error(f"Error in button callback '{callback_str}': {e}")
                    
                    field = FieldFactory.create_field(parent, field_data, callback)
                else:
                    field = FieldFactory.create_field(parent, field_data)
                
                # Create the widget
                widget_container = field.create()
                widget_container.pack(fill=tk.BOTH, expand=True, pady=5)
                
                # Store field reference (skip dividers)
                if field_data['type'] != 'divider':
                    self.fields.append(field)
                
                # Track first focusable widget
                if self.first_focusable_widget is None:
                    focusable_types = ['text', 'multiline', 'selection']
                    if field_data['type'] in focusable_types:
                        self.first_focusable_widget = field.widget
                
            except Exception as e:
                logger.error(f"Failed to create field {field_data.get('name', 'unknown')}: {e}")
                raise

    def _on_ok(self):
        """Handle OK button click."""
        try:
            self.result = self.values
            logger.info(f"Dialog OK clicked with values: {self.result}")
            self.root.destroy()
        except Exception as e:
            logger.error(f"Error getting dialog values: {e}")
            self.result = None
            self.root.destroy()

    def _on_cancel(self):
        """Handle Cancel button click."""
        self.result = None
        logger.info("Dialog cancelled")
        self.root.destroy()

    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        
        # Get window dimensions
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"+{x}+{y}")


def create_dialog(template: Union[str, Path]) -> Dialog:
    """Convenience function to create a Dialog instance."""
    return Dialog(template)

