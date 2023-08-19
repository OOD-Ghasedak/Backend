import os
import shutil
from typing import Optional

from django.conf import settings
from rest_framework.test import APITestCase, APIClient

from accounts.models.services.ghased_creation import GhasedCreatorConfigurer, GhasedData


def check_wrapper(client_request_function):
    def raise_or_return_response(response, assert_status_code: Optional[int]):
        if assert_status_code is not None:
            if assert_status_code != response.status_code:
                msg = f'expected: {assert_status_code}, actual: {response.status_code}'
                if response.status_code == 400:
                    msg += 'json:' + str(response.json())
                assert assert_status_code == response.status_code, msg
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


class OpenFileForTestHelper:

    def __delete_files_inside_folder(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def _delete_files_inside_media_folder(self):
        # pass
        self.__delete_files_inside_folder(folder=settings.MEDIA_ROOT)

    def __call__(self, file_path):
        def test_func_wrapper(test_func):
            def wrapped_test_func(self_, *args, **kwargs):
                _oppened_files = getattr(self_, '_opened_files', [])
                with open(file_path, mode='rb') as f:
                    _oppened_files.append(f)
                    setattr(self_, '_opened_files', _oppened_files)
                    result = test_func(self_, *args, **kwargs)
                self._delete_files_inside_media_folder()
                return result
            return wrapped_test_func
        return test_func_wrapper


open_file_for_test = OpenFileForTestHelper()