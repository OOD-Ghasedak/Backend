from django.test import tag

from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestChangePassword(GhasedTestCase):
    change_password_url = '/api/accounts/change-password/'

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)

    @tag('unit_api')
    def test_change_password_failed(self):
        self.assertTrue(self.ghased.user.check_password('my_secured_password'))
        response = self.client.post(
            self.change_password_url,
            data={
                'old_password': 'wrong',
                'new_password': 'security12'
            },
            HTTP_AUTHORIZATION=self.jwt_token,
            assert_status_code=400,
            format='json',
        )
        self.assertIn('اشتباه است', response.json()['message'])

    @tag('unit_api')
    def test_change_password(self):
        password = 'my_secured_password'
        new_password = 'more_secured_password'
        self.assertTrue(self.ghased.user.check_password(password))
        response = self.client.post(
            self.change_password_url,
            data={
                'old_password': password,
                'new_password': new_password,
            },
            HTTP_AUTHORIZATION=self.jwt_token,
            assert_status_code=200,
            format='json',
        )
        self.ghased.refresh_from_db()
        self.assertFalse(self.ghased.user.check_password(password))
        self.assertTrue(self.ghased.user.check_password(new_password))


