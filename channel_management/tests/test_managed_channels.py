from django.test import tag

from channel_management.models import ChannelOwner
from channels.models import Channel
from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestManagedChannels(GhasedTestCase):
    managed_channels_url = '/api/channel-management/managed-channels/'

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)

    @tag('unit_api')
    def test_get_subscribed_channels(self):
        my_channels = []
        my_channels.append(Channel.objects.create(name='my_channel'))
        for i in range(3):
            Channel.objects.create(name=f'not_my_channel{i + 1}')
        my_channels.append(Channel.objects.create(name='my_channel2'))
        for mc in my_channels:
            ChannelOwner.objects.create(channel=mc, ghased=self.ghased)

        data = self.client.get(
            f'{self.managed_channels_url}',
            HTTP_AUTHORIZATION=self.jwt_token,
            format='json',
            assert_status_code=200,
        ).json()
        self.assertEqual(
            {obj['id'] for obj in data},
            {c.id for c in my_channels},
        )
