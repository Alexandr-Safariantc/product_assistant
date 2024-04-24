from django.conf import settings
from django.core.exceptions import ValidationError


def validate_ingredient_amount(amount: int):
    """Return error for invalid ingredient amount value."""
    if amount > settings.INGREDIENT_AMOUNT_MAX:
        raise ValidationError(
            settings.COOKING_TIME_INGREDIENT_AMOUNT_TOO_HIGH.format(
                field_name='Количество ингредиента'
            ))
    elif amount < settings.INGREDIENT_AMOUNT_MIN:
        raise ValidationError(
            settings.COOKING_TIME_INGREDIENT_AMOUNT_TOO_LOW.format(
                field_name='Количество ингредиента',
                min_value=settings.INGREDIENT_AMOUNT_MIN
            ))


def validate_cooking_time(minutes: int):
    """Return error if cooking_time is less 1 and greater max value."""
    if minutes < settings.COOKING_TIME_MIN_MINUTES:
        raise ValidationError(
            settings.COOKING_TIME_INGREDIENT_AMOUNT_TOO_LOW.format(
                field_name='Время приготовления',
                min_value=settings.COOKING_TIME_MIN_MINUTES
            ))
    elif minutes > settings.COOKING_TIME_MAX_MINUTES:
        raise ValidationError(
            settings.COOKING_TIME_INGREDIENT_AMOUNT_TOO_HIGH.format(
                field_name='Время приготовления',
            ))
