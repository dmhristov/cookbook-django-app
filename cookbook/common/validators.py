from django.core.exceptions import ValidationError


def name_contains_only_letters_validator(value):
    if not value.isalpha():
        raise ValidationError('Name must contain only letters!')

