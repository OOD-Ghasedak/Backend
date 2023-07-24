from django.core.validators import MinValueValidator
from django.db import models


def LocationCordinationField(**kwargs):
    """
    example:
        long/lat = LocationCordinationField(
            verbose_name='عرض جغرافیایی',
            null=True,
            blank=True,
        )
    """
    defaults = dict(
        max_digits=9,
        decimal_places=6,
    )
    defaults.update(kwargs)
    return models.DecimalField(
        defaults
    )


class PositiveFloatField(models.FloatField):
    default_validators = [MinValueValidator(0)]

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            **kwargs,
        })


class PercentageField(PositiveFloatField):
    default_validators = [*PositiveFloatField.default_validators, MinValueValidator(100)]

    def formfield(self, **kwargs):
        return super().formfield(**{
            'max_value': 100,
            **kwargs,
        })
