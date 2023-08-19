from typing import List, Callable

from django.conf import settings
from rest_framework.serializers import SerializerMetaclass


class SecuredFileSerializerMetaclass(SerializerMetaclass):
    validator_generators = []
    extra_validators: List[Callable]
    file_security_context_key = 'file_security'

    @classmethod
    def _get_validator_generators(cls):
        return cls.validator_generators

    @classmethod
    def generate_validate_file_function(cls, file_field: str):
        validators = [
                         getattr(cls, validator_generator)(file_field)
                         for validator_generator in cls._get_validator_generators()
                     ] + cls.extra_validators

        def validate_file(self, file):
            for validator in validators:
                validator(self, file, file_field)
            return file

        return validate_file

    @classmethod
    def _set_from_serializer_class(cls, serializer_class: "SecuredFileSerializerMetaclass"):
        cls.file_security_context_key = getattr(serializer_class, 'file_security_context_key', cls.file_security_context_key)
        cls.extra_validators = getattr(serializer_class, 'file_security_extra_validators', [])

    def __new__(cls, name, bases, attrs):
        serializer_class = super().__new__(cls, name, bases, attrs)
        if not settings.SECURE_FILE_HANDLING_APIS:
            return serializer_class
        cls._set_from_serializer_class(serializer_class)
        securing_file_fields: List[str] = getattr(serializer_class, 'securing_file_fields', [])
        for securing_file_field in securing_file_fields:
            setattr(serializer_class, f'validate_{securing_file_field}',
                    cls.generate_validate_file_function(securing_file_field))
        return serializer_class

    @classmethod
    def update_context(cls, serializer, **kwargs):
        serializer.context[cls.file_security_context_key] = {
            **serializer.context.get(cls.file_security_context_key, {}),
            **kwargs
        }
