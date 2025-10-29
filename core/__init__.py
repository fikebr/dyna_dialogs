"""Dynamic Dialog System - Create tkinter dialogs from simple text templates."""

from core.dialog import Dialog, create_dialog
from core.parser import TemplateParser
from core.fields import FieldFactory

__all__ = ['Dialog', 'create_dialog', 'TemplateParser', 'FieldFactory']

