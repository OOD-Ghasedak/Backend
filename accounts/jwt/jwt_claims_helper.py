from typing import Union, List, Tuple

from rest_framework.fields import get_attribute


class JWTClaimsHelper:

    def __init__(self, user, jwt_claim_keys: List[Union[str, Tuple[str, str]]]):
        self.user = user
        self.jwt_claim_keys = jwt_claim_keys

    def get_jwt_claims(self):
        claims = dict()
        for claim_key in set(self.jwt_claim_keys):
            if isinstance(claim_key, (tuple, list)) and len(claim_key) == 2:
                field_name, claim_key = claim_key
            elif isinstance(claim_key, str):
                field_name, claim_key = claim_key, claim_key
            else:
                raise ValueError('claim key must be a <field_name, claim_key> tuple or an instance of str')
            claims[claim_key] = get_attribute(self.user, field_name)
        return claims
