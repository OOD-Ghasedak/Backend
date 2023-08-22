from django.test import tag

from channel_management.models import ChannelOwner, ChannelAdmin
from channels.models import Channel
from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestManagedAdmin(GhasedTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)
        self.channel = Channel.objects.create(name='unit+test')
        self.owner = ChannelOwner.objects.create(channel=self.channel, ghased=self.ghased)
        self.random_ghased = self.create_random_ghased()

    @tag('integrated_api')
    def test_make_admin(self):
        self.client.post(
            f'/api/channel-management/{self.channel.id}/admins/',
            data={
                'ghased': self.random_ghased.id,
                'share': 20,
            },
            assert_status_code=201,
            HTTP_AUTHORIZATION=self.jwt_token,
        )
        admin = self.channel.get_ghased_status_wrt_channel(self.random_ghased)
        self.assertTrue(isinstance(admin, ChannelAdmin))
        self.assertEqual(admin.share, 20)
        self.client.patch(
            f'/api/channel-management/admins/{admin.id}/',
            data={
                'share': 50,
            },
            assert_status_code=200,
            HTTP_AUTHORIZATION=self.jwt_token,
        )
        admin.refresh_from_db()
        self.assertEqual(admin.share, 50)

