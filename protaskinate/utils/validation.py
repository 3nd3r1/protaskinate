"""protaskinate/utils/validation.py"""

def validate_enum(value, enum_class, field_name):
    """Validate that a value is a member of an enumeration."""
    try:
        return enum_class(value)
    except ValueError as exc:
        raise ValueError(f"Invalid {field_name}: {value}") from exc

def validate_type(value, expected_type, field_name, allow_none=False):
    """Validate that a value is of the expected type."""
    if not isinstance(value, expected_type) and not (allow_none and value is None):
        raise ValueError(f"Invalid {field_name}: {value}")
