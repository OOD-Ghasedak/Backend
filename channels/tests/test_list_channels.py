from django.test import tag

from channel_management.models import ChannelOwner
from channels.models import Channel
from subscribe.models import Subscriber
from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestListChannels(GhasedTestCase):
    _channels_url = None
    _channels_url_template = '/api/channels/{pk}/'.format

    @property
    def channels_url(self):
        return self._channels_url

    @channels_url.setter
    def channels_url(self, pk):
        self._channels_url = self._channels_url_template(pk=str(pk))

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)
        self.channel = Channel.objects.create(name='unit+test')
        self.owner = ChannelOwner.objects.create(channel=self.channel, ghased=self.create_random_ghased())

    @tag('unit_api')
    def test_retrieve_channel(self):
        self.channels_url = self.channel.id
        data = self.client.get(
            f'{self.channels_url}',
            HTTP_AUTHORIZATION=self.jwt_token,
            assert_status_code=200,
        ).json()
        self.assertFalse(data['has_subscription'])
        self.assertEqual(data['role'], 'viewer')
        Subscriber.objects.create(channel=self.channel, ghased=self.ghased)
        data = self.client.get(
            f'{self.channels_url}',
            HTTP_AUTHORIZATION=self.jwt_token,
            assert_status_code=200,
        ).json()
        self.assertEqual(data['role'], 'subscriber')

