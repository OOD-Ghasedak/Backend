import dataclasses

from django.test import tag

from accounts.models import RegisterOTP, Ghased
from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestSignUpGhased(GhasedTestCase):
    signup_url = '/api/accounts/signup/'
    verifY_signup_url = '/api/accounts/verify-signup/'

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)

    @dataclasses.dataclass
    class TestUserData:
        username: str
        password: str
        otp: str

    def successfully_create_ghased(self, user_data: TestUserData):
        response = self.client.post(
            f'{self.signup_url}',
            data=dataclasses.asdict(user_data),
            assert_status_code=201,
            format='json',
        )
        self.assertTrue(Ghased.objects.filter(user__username=user_data.username).exists())
        return response

    @tag('unit_api')
    def test_sign_up(self) -> None:
        otp = RegisterOTP.generate_register_otp(email=None, phone_number='09396588871')

        user_data = self.TestUserData(username='ashkan.khd', password='1223', otp=otp.code)
        self.successfully_create_ghased(user_data)

        otp = RegisterOTP.generate_register_otp(email='ashkan.khd.q@gmail.com', phone_number=None)
        user_data = self.TestUserData(username='ashkan.khd1', password='1223', otp=otp.code)
        self.successfully_create_ghased(user_data)

    @tag('unit_api')
    def test_verify_sign_up(self):
        email = 'ashkan.khd.q@gmail.com'
        self.assertFalse(RegisterOTP.objects.filter(email=email).exists())
        response = self.client.post(
            f'{self.verifY_signup_url}',
            data={
                'email': email,
                'phone_number': None
            },
            assert_status_code=201,
            format='json',
        )
        self.assertTrue(RegisterOTP.objects.filter(email=email).exists())
        self.assertIsNotNone(response.json()['otp'])
