from typing import Optional

from rest_framework.test import APITestCase, APIClient

from accounts.models.services.ghased_creation import GhasedCreatorConfigurer, GhasedData


def check_wrapper(client_request_function):
    def raise_or_return_response(response, assert_status_code: Optional[int]):
        if assert_status_code is not None:
            assert assert_status_code == response.status_code, \
                f'expected: {assert_status_code}, actual: {response.status_code}'
        return response

    def check_and_request(*args, **kwargs):
        assert_status_code: Optional[int] = kwargs.pop('assert_status_code', None)
        return raise_or_return_response(
            client_request_function(*args, **kwargs),
            assert_status_code
        )

    return check_and_request


class APIClientCheckingDecorator(APIClient):
    def __init__(self, client: APIClient):
        self.decoratee = client

    def __getattribute__(self, item):
        if item == 'decoratee':
            return super().__getattribute__(item)
        attr = getattr(self.decoratee, item)
        if item in ['get', 'post', 'put', 'patch', 'delete', 'options']:
            attr = check_wrapper(attr)
        return attr


class GhasedTestCase(APITestCase):
    @property
    def jwt_token(self):
        return f'JWT {self.jwt_access_token}'

    def setUp(self) -> None:
        self.ghased = GhasedCreatorConfigurer(source=GhasedCreatorConfigurer.Sources.TEST).configure(
            GhasedData('test_user', '09123456789', 'test@ghasedak.ir', 'my_secured_password'),
        ).create()
        self.jwt_refresh_token, self.jwt_access_token = self.ghased.get_jwt_tokens()
