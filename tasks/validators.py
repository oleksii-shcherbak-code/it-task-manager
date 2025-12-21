import re
from django.core.exceptions import ValidationError


def validate_username(value) -> None:
    """Validate username: only Latin letters, digits, max one underscore, length 3–30."""
    if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", value):
        raise ValidationError(
            "Username must contain only Latin letters, digits and at most one underscore."
        )
    if value.count("_") > 1:
        raise ValidationError("Username may contain at most one underscore.")


def validate_only_letters(value) -> None:
    """Validate that field contains only letters (Latin or Cyrillic)."""
    if not value.isalpha():
        raise ValidationError("This field can only contain letters.")
