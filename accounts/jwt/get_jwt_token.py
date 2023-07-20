import typing
from typing import Tuple

from rest_framework_simplejwt.tokens import RefreshToken

if typing.TYPE_CHECKING:
    from accounts.models import Ghased


def get_jwt_token(ghased: 'Ghased') -> Tuple[str, str]:
    token = RefreshToken.for_user(ghased.user)
    for claim_key, claim_val in ghased.get_jwt_claims().items():
        token[claim_key] = claim_val
    refresh, access = str(token), str(token.access_token)
    return refresh, access
