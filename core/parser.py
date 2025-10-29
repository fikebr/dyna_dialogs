"""Template parser for dynamic dialogs."""

import logging
import os
from pathlib import Path
from typing import Dict, List, Union

logger = logging.getLogger(__name__)


class TemplateParser:
    """Parses pipe-delimited dialog templates."""

    def __init__(self, template: Union[str, Path]):
        """Initialize parser with template string or file path."""
        self.template_str = self._load_template(template)
        self.title = ""
        self.size = None
        self.fields = []

    def _load_template(self, template: Union[str, Path]) -> str:
        """Auto-detect file path vs string and load template content."""
        # Convert to string if Path object
        if isinstance(template, Path):
            template = str(template)

        # Check if it looks like a file path
        if isinstance(template, str):
            # If it contains newlines, it's likely a template string
            if '\n' in template:
                logger.debug("Template detected as string input")
                return template

            # Check if file exists
            if os.path.isfile(template):
                logger.info(f"Loading template from file: {template}")
                try:
                    with open(template, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    logger.error(f"Failed to read template file: {e}")
                    raise

            # If no newlines and file doesn't exist, treat as string
            logger.debug("Template detected as string input")
            return template

        raise ValueError("Template must be a string or Path object")

    def parse(self) -> Dict:
        """Parse the template and return structured data."""
        lines = [line.strip() for line in self.template_str.strip().split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines

        if not lines:
            raise ValueError("Template is empty")

        # Parse first line as title|size
        self._parse_header(lines[0])

        # Parse remaining lines as fields
        for i, line in enumerate(lines[1:], start=2):
            try:
                self._parse_field(line)
            except Exception as e:
                logger.error(f"Error parsing line {i}: {line} - {e}")
                raise ValueError(f"Invalid field format at line {i}: {line}") from e

        return {
            'title': self.title,
            'size': self.size,
            'fields': self.fields
        }

    def _parse_header(self, line: str):
        """Parse the header line (title|size)."""
        parts = line.split('|')
        
        if len(parts) < 1:
            raise ValueError("Header must contain at least a title")

        self.title = parts[0].strip()

        # Parse size if provided (format: WxH or HxW)
        if len(parts) > 1 and parts[1].strip():
            size_str = parts[1].strip()
            if 'x' in size_str.lower():
                try:
                    width, height = size_str.lower().split('x')
                    self.size = (int(width.strip()), int(height.strip()))
                    logger.debug(f"Parsed size: {self.size}")
                except ValueError:
                    logger.warning(f"Invalid size format: {size_str}, using default")
                    self.size = None
            else:
                logger.warning(f"Invalid size format: {size_str}, expected WxH")

    def _parse_field(self, line: str):
        """Parse a field line (name|type|options)."""
        parts = [p.strip() for p in line.split('|')]

        if len(parts) < 2:
            raise ValueError(f"Field must have at least name and type: {line}")

        field_name = parts[0]
        field_type = parts[1]

        # Extract options (everything after type, comma-separated)
        options = []
        callback = None
        if len(parts) > 2:
            # Join all parts after type and split by comma
            options_str = '|'.join(parts[2:])
            if options_str:
                # For button fields, treat the third part as callback instead of options
                if field_type == 'button':
                    callback = options_str.strip()
                else:
                    options = [opt.strip() for opt in options_str.split(',')]

        # Validate field type
        valid_types = ['text', 'multiline', 'selection', 'checkgroup', 'radio', 'button', 'divider']
        if field_type not in valid_types:
            raise ValueError(f"Invalid field type: {field_type}. Must be one of {valid_types}")

        field_data = {
            'name': field_name,
            'type': field_type,
            'options': options
        }
        
        # Add callback for button fields
        if callback:
            field_data['callback'] = callback

        self.fields.append(field_data)
        logger.debug(f"Parsed field: {field_data}")

