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
