from django.core.exceptions import ValidationError
import re


def validate_hex_str(s):
    if not re.match('[0-9a-fA-F]+', s):
        raise ValidationError()
