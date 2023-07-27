from django.test import tag

from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestGhasedProfile(GhasedTestCase):
    profile_url = '/api/accounts/profile/'

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)

    def test_get_profile(self):
        data = self.client.get(
            f'{self.profile_url}',
            HTTP_AUTHORIZATION=self.jwt_token,
            assert_status_code=200,
        ).json()
        self.assertEqual(data['email'], self.ghased.user.email)
