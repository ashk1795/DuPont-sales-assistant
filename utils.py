"""
Utility functions for Tedlar LeadGen.
"""

def validate_email(email):
    """
    Validate an email address format.
    Args:
        email (str): Email address to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    # TODO: Implement email validation logic
    return "@" in email and "." in email 