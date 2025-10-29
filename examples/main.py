"""Example usage of the Dynamic Dialog System.

This example demonstrates how to use dyna-dialogs after installation.

Installation:
    pip install git+https://github.com/fikebr/dyna-dialogs.git

    # Or with optional logger utilities:
    pip install "dyna-dialogs[logger] @ git+https://github.com/fikebr/dyna-dialogs.git"

Note: This example uses the optional logger utilities. 
If you installed without [logger], comment out the ProjectLogger lines 
and use standard Python logging setup instead.
"""

import logging
from pathlib import Path

# Import from installed package
from core import Dialog, create_dialog
from utils.logger import ProjectLogger

# Module-level logger (will be initialized in main)
logger = logging.getLogger(__name__)


def reset_callback(dialog):
    """Example callback for the reset button."""
    logger.info("Reset button clicked!")
    logger.info(f"Current dialog values: {dialog.values}")
    
    # Example: Set field values
    dialog.set_field_value("username", "test")
    dialog.set_field_value("bio", "This is a test bio")
    dialog.set_field_value("theme", "dark")
    dialog.set_field_value("notifications", "email,sms")  # Comma-delimited for checkgroup
    dialog.set_field_value("role", "admin")
    
    logger.info(f"Updated dialog values: {dialog.values}")


def custom_action_callback(dialog):
    """Example callback for custom action button."""
    logger.info("Custom action button clicked!")
    values = dialog.values
    logger.info(f"User: {values.get('username', 'N/A')}")
    logger.info(f"Role: {values.get('role', 'N/A')}")


def example_string_template():
    """Example using a string template."""
    logger.info("\n" + "="*60)
    logger.info("Example 1: String Template")
    logger.info("="*60)
    
    template = """
User Settings|500x450
username|text
bio|multiline
theme|selection|light,dark,auto
notifications|checkgroup|email,sms,push
role|radio|admin,user,guest
reset|button|main.reset_callback
|divider
custom_action|button|main.custom_action_callback
"""
    
    try:
        dialog = Dialog(template)
        result = dialog.show()
        
        if result:
            logger.info("Dialog returned values:")
            for key, value in result.items():
                logger.info(f"  {key}: {value}")
        else:
            logger.info("Dialog was cancelled")
            
    except Exception as e:
        logger.error(f"Error creating dialog: {e}", exc_info=True)


def example_file_template():
    """Example using a template file."""
    logger.info("\n" + "="*60)
    logger.info("Example 2: File Template")
    logger.info("="*60)
    
    # Create a sample template file
    template_content = """
Login Form|400x300
username|text
password|text
remember|checkgroup|Remember me
|divider
"""
    
    template_file = Path("sample_template.txt")
    
    try:
        # Write template file
        with open(template_file, 'w') as f:
            f.write(template_content)
        
        logger.info(f"Created template file: {template_file}")
        
        # Create dialog from file
        dialog = create_dialog(template_file)
        result = dialog.show()
        
        if result:
            logger.info("Login form returned:")
            for key, value in result.items():
                logger.info(f"  {key}: {value}")
        else:
            logger.info("Login cancelled")
            
    except Exception as e:
        logger.error(f"Error with file template: {e}", exc_info=True)
    finally:
        # Clean up template file
        if template_file.exists():
            template_file.unlink()
            logger.info(f"Removed template file: {template_file}")


def example_simple_dialog():
    """Example of a simple dialog without custom buttons."""
    logger.info("\n" + "="*60)
    logger.info("Example 3: Simple Contact Form")
    logger.info("="*60)
    
    template = """
Contact Information|450x350
full_name|text
email|text
phone|text
preferred_contact|radio|email,phone,either
message|multiline
"""
    
    try:
        result = create_dialog(template).show()
        
        if result:
            logger.info("Contact form submitted:")
            for key, value in result.items():
                logger.info(f"  {key}: {value}")
        else:
            logger.info("Contact form cancelled")
            
    except Exception as e:
        logger.error(f"Error with simple dialog: {e}", exc_info=True)


def main():
    """Run example dialogs."""
    # Setup logging
    ProjectLogger(keep=7, level=logging.DEBUG).init()
    
    logger.info("Starting Dynamic Dialog Examples")
    
    try:
        # Run examples
        example_simple_dialog()
        example_string_template()
        example_file_template()
        
        logger.info("\n" + "="*60)
        logger.info("All examples completed successfully!")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}", exc_info=True)


if __name__ == "__main__":
    main()
