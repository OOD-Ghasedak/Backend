from typing import List, TYPE_CHECKING

import magic
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from utility.django import is_unsafe, safe_it
from utility.python import common_prefix, rand_slug

if TYPE_CHECKING:
    from utility.api_file_handling.serializer_metaclass import SecuredFileSerializerMetaclass
    from rest_framework.serializers import Serializer


class SecureFileMixinBase:

    @classmethod
    def generate_error_message(cls, error_template: str, error_template_kwargs: dict):
        return error_template.format(error_template_kwargs)


class SecureFileTypeMixin(SecureFileMixinBase):
    accepted_mime_types: List[str]
    WRONG_TYPE_EXCEPTION_MESSAGE = 'محتوا از این نوع قابل پذیرش نیست!'
    DIFFERENT_TYPE_EXTENSION_WITH_TYPE_EXCEPTION_MESSAGE = 'نوع محتوا با اکستنشن آن در تضاد است!'

    @classmethod
    def get_validate_file_type(cls, file_field: str):

        def validate_file_type(serializer: "Serializer", file: InMemoryUploadedFile, field_name: str):
            if not file:
                return
            file.seek(0)
            mime_type = magic.from_buffer(file.read(), mime=True)
            error_template_kwargs = dict(
                file_type=mime_type,
                field_name=field_name
            )
            file.seek(0)
            if mime_type not in cls.accepted_mime_types:
                raise ValidationError([
                    cls.generate_error_message(cls.WRONG_TYPE_EXCEPTION_MESSAGE, error_template_kwargs)
                ])
            same_type_ignoring_subtype = file.content_type.split('/')[0] == mime_type.split('/')[0]
            if not same_type_ignoring_subtype:
                raise ValidationError([
                    cls.generate_error_message(cls.DIFFERENT_TYPE_EXTENSION_WITH_TYPE_EXCEPTION_MESSAGE, error_template_kwargs)
                ])
            cls.update_context(serializer, file_type=mime_type)

        return validate_file_type

    @classmethod
    def _set_from_serializer_class(cls, serializer_class: "SecuredFileSerializerMetaclass"):
        super()._set_from_serializer_class(serializer_class)
        cls.accepted_mime_types = getattr(serializer_class, 'accepted_mime_types', [])


class SecureFileNameMixin(SecureFileMixinBase):
    BAD_FILE_NAME_MESSAGE = 'نام فایل غیرمجاز است!'
    FILE_NAME_SECURITY_MODE_RAISE = 'RAISE'
    FILE_NAME_SECURITY_MODE_CHANGE_NAME = 'CHANGE_NAME'
    security_mode = FILE_NAME_SECURITY_MODE_CHANGE_NAME

    @classmethod
    def find_file_extension(cls, serializer: "Serializer", file: InMemoryUploadedFile):
        serializer_context: dict = getattr(serializer, 'context', {})
        mime_type = serializer_context.get(cls.context_key, {}).get('file_type')
        if mime_type:
            return mime_type.split('/')[-1]
        extension = file.name.split('.')[-1]
        if extension and extension != file.name:
            return extension

    @classmethod
    def generate_safe_file_name(cls, serializer: "Serializer", file: InMemoryUploadedFile):
        options = []
        common = common_prefix(file.name, safe_it(file.name))
        if common:
            options.append(common)
        else:
            options.append(rand_slug()[:4])
        options.append(timezone.now().strftime("%Y_%m_%dT%H_%M_%S_%f"))
        safe_name = '-'.join(options)
        extension = cls.find_file_extension(serializer, file)
        if extension:
            safe_name += f'.{extension}'
        return safe_name

    @classmethod
    def get_validate_file_name(cls, file_field: str):
        def validate_file_name(serializer: "Serializer", file: InMemoryUploadedFile, field_name: str):
            if not file:
                return
            if is_unsafe(file.name):
                if cls.security_mode == cls.FILE_NAME_SECURITY_MODE_RAISE:
                    raise ValidationError([
                        cls.generate_error_message(
                            cls.BAD_FILE_NAME_MESSAGE, dict(file_name=file.name, field_name=field_name)
                        )
                    ])
                elif cls.security_mode == cls.FILE_NAME_SECURITY_MODE_CHANGE_NAME:
                    file.name = cls.generate_safe_file_name(serializer, file)
            cls.update_context(serializer, file_name=file.name)
        return validate_file_name

    @classmethod
    def _set_from_serializer_class(cls, serializer_class: "SecuredFileSerializerMetaclass"):
        super()._set_from_serializer_class(serializer_class)
        cls.security_mode = getattr(serializer_class, 'file_name_security_mode', cls.security_mode)


class SecureFileSizeMixin(SecureFileMixinBase):
    file_size_limit: int
    FILE_SIZE_EXCEEDED_MESSAGE = 'حجم فایل خیلی زیاد است!'

    @classmethod
    def _set_from_serializer_class(cls, serializer_class: "SecuredFileSerializerMetaclass"):
        super()._set_from_serializer_class(serializer_class)
        cls.file_size_limit = getattr(serializer_class, 'file_size_limit', [])

    @staticmethod
    def _get_file_size(file: InMemoryUploadedFile):
        return file.size

    @classmethod
    def get_validate_file_size(cls, file_field: str):
        file_size_limit = cls.file_size_limit

        def validate_file_name(serializer: "Serializer", file: InMemoryUploadedFile, field_name: str):
            if not file:
                return
            file_size = cls._get_file_size(file)
            if file_size > file_size_limit:
                raise ValidationError([
                    cls.generate_error_message(
                        cls.FILE_SIZE_EXCEEDED_MESSAGE, dict(file_size=file_size, field_name=field_name)
                    )
                ])
            cls.update_context(serializer, file_size=file_size)

        return validate_file_name
