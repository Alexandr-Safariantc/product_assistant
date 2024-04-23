from django.core.exceptions import ValidationError

from foodgram_backend.settings import (
    COOKING_TIME_INGREDIENT_AMOUNT_TOO_LOW,
    COOKING_TIME_INGREDIENT_AMOUNT_TOO_HIGH,
    COOKING_TIME_MAX_MINUTES,
    COOKING_TIME_MIN_MINUTES,
    INGREDIENT_AMOUNT_MAX,
    INGREDIENT_AMOUNT_MIN,
)


def validate_ingredient_amount(amount: int):
    """Return error for invalid ingredient amount value."""
    if amount > INGREDIENT_AMOUNT_MAX:
        raise ValidationError(COOKING_TIME_INGREDIENT_AMOUNT_TOO_HIGH.format(
            field_name='Количество ингредиента'
        ))
    elif amount < INGREDIENT_AMOUNT_MIN:
        raise ValidationError(COOKING_TIME_INGREDIENT_AMOUNT_TOO_LOW.format(
            field_name='Количество ингредиента',
            min_value=INGREDIENT_AMOUNT_MIN
        ))


def validate_cooking_time(minutes: int):
    """Return error if cooking_time is less 1 and greater max value."""
    if minutes < COOKING_TIME_MIN_MINUTES:
        raise ValidationError(COOKING_TIME_INGREDIENT_AMOUNT_TOO_LOW.format(
            field_name='Время приготовления',
            min_value=COOKING_TIME_MIN_MINUTES
        ))
    elif minutes > COOKING_TIME_MAX_MINUTES:
        raise ValidationError(COOKING_TIME_INGREDIENT_AMOUNT_TOO_HIGH.format(
            field_name='Время приготовления',
        ))
