import typing
from typing import Union, List, Tuple, Any

from django.contrib.auth.models import User
from rest_framework.fields import get_attribute
from rest_framework_simplejwt.tokens import RefreshToken

if typing.TYPE_CHECKING:
    from accounts.models import Ghased


class JWTHelper:
    jwt_user: Any
    jwt_claim_keys: List[Union[str, Tuple[str, str]]]

    def get_user_for_claims(self) -> Any:
        return self.jwt_user

    def get_user_for_token(self) -> Any:
        return self.jwt_user

    def get_jwt_claims(self):
        claims = dict()
        for claim_key in set(self.jwt_claim_keys):
            if isinstance(claim_key, (tuple, list)) and len(claim_key) == 2:
                field_name, claim_key = claim_key
            elif isinstance(claim_key, str):
                field_name, claim_key = claim_key, claim_key
            else:
                raise ValueError('claim key must be a <field_name, claim_key> tuple or an instance of str')
            claims[claim_key] = get_attribute(self.get_user_for_claims(), field_name.split('.'))
        return claims

    def get_jwt_tokens(self) -> Tuple[str, str]:
        token = RefreshToken.for_user(self.get_user_for_token())
        for claim_key, claim_val in self.get_jwt_claims().items():
            token[claim_key] = claim_val
        refresh, access = str(token), str(token.access_token)
        return refresh, access


class GhasedJWTHelper(JWTHelper):
    jwt_claim_keys = [
        ('id', 'ghased_id'),
        ('user.id', 'user_id'),
        ('user.username', 'username'),
    ]

    def __init__(self, ghased: 'Ghased'):
        self.jwt_user = ghased

    def get_user_for_token(self) -> User:
        return self.jwt_user.user
