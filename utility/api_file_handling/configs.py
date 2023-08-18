from utility.api_file_handling.mixins import SecureFileTypeMixin, SecureFileNameMixin, SecureFileSizeMixin
from utility.api_file_handling.serializer_metaclass import SecuredFileSerializerMetaclass


class ConfiguredSecuredFileSerializerMeta(
    SecureFileSizeMixin,
    SecureFileNameMixin,
    SecureFileTypeMixin,
    SecuredFileSerializerMetaclass,
):
    validator_generators = [
        'get_validate_file_type',
        'get_validate_file_name',
        'get_validate_file_size',
    ]
