import dataclasses
from typing import List, Tuple, Dict

from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.safestring import mark_safe
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
    def _get_choices(cls) -> List[Choice]:
        choices = []
        vars_ = vars(cls)
        for attr in vars_:
            attribute = vars_[attr]
            if isinstance(attribute, cls.Choice):
                choices.append(attribute)
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


unsafe_chars_translator = {
    ord('\\'): '\\u005C',
    ord('\''): '\\u0027',
    ord('='): '\\u003D',
    ord('-'): '\\u002D',
    ord(';'): '\\u003B',
    ord('`'): '\\u0060',
    ord('\u2028'): '\\u2028',
    ord('\u2029'): '\\u2029',
    ord('&'): '&amp;',
    ord('<'): '&lt;',
    ord('>'): '&gt;',
    ord('"'): '&quot;',
    ord("'"): '&#39;',
}
unsafe_chars_translator.update((ord('%c' % z), '\\u%04X' % z) for z in range(32))


def safe_it(unsafe_input: str) -> str:
    return mark_safe(str(unsafe_input).translate(unsafe_chars_translator))


def is_unsafe(unknown_input: str) -> bool:
    return safe_it(unknown_input) != unknown_input
