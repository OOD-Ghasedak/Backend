from django.test import tag

from channel_management.models import ChannelOwner
from channels.models import Channel
from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestSubscibeUnsubscribe(GhasedTestCase):
    _subscribe_url = None
    _subscribe_url_template = '/api/subscribe/{pk}/'.format

    @property
    def subscribe_url(self):
        return self._subscribe_url

    @subscribe_url.setter
    def subscribe_url(self, pk):
        self._subscribe_url = self._subscribe_url_template(pk=str(pk))

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)
        self.channel = Channel.objects.create(name='unit+test')
        self.owner = ChannelOwner.objects.create(channel=self.channel, ghased=self.create_random_ghased())

    @tag('integrated_api')
    def test_subscribe(self):
        self.subscribe_url = self.channel.id
        self.client.post(
            self.subscribe_url,
            assert_status_code=201,
            HTTP_AUTHORIZATION=self.jwt_token,
            format='json',
        )
        data = self.client.post(
            self.subscribe_url,
            assert_status_code=424,
            HTTP_AUTHORIZATION=self.jwt_token,
            format='json',
        )
        self.assertIn('message', data.json())
