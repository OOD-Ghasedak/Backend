import dataclasses
from typing import List, Tuple, Dict

from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class GhasedakMobileNumberValidator(BaseValidator):
    message = _('Ensure your phone number has 11 digits starting with 09')
    code = 'mobile_number_value'

    def __init__(self, message=None):
        super().__init__(None, message)

    def compare(self, cleaned_value, limit_value):
        return cleaned_value.isnumeric() and len(cleaned_value) == 11 and cleaned_value.startswith('09')

    def clean(self, not_cleaned_value):
        return str(not_cleaned_value)


class MA(type):
    def __getattribute__(cls, attribute):
        print('fuck')
        return super().__getattribute__(attribute)


class ChoicesMeta(type):
    REAL_ACCESS_TO_CHOICE_FLAG = '__real'

    def __getattribute__(cls, item: str):
        if item in ['Choice', 'REAL_ACCESS_TO_CHOICE_FLAG']:
            return super().__getattribute__(item)

        if item.startswith(cls.REAL_ACCESS_TO_CHOICE_FLAG):
            return super().__getattribute__(item.lstrip(cls.REAL_ACCESS_TO_CHOICE_FLAG))
        attr = super().__getattribute__(item)
        if isinstance(attr, Choices.Choice):
            return attr.value
        return attr


class Choices(metaclass=ChoicesMeta):
    @dataclasses.dataclass
    class Choice:
        value: str
        fa_value: str

    @classmethod
    def real_access_to_choice(cls, choice_name: str):
        return getattr(cls, f'{cls.REAL_ACCESS_TO_CHOICE_FLAG}{choice_name}')

    @classmethod
    def _get_choices(cls) -> List[Choice]:
        choices = []
        for attr in vars(cls):
            if attr.startswith('__'):
                continue
            choices.append(cls.real_access_to_choice(attr))
        return choices

    @classmethod
    def get_choices(cls) -> Tuple[Tuple[str, str], ...]:
        choices = []
        for choice in cls._get_choices():
            choices.append(
                (choice.value, choice.fa_value)
            )
        return tuple(choices)

    @classmethod
    def get_translator(cls) -> Dict[str, str]:
        return dict(cls.get_choices())
