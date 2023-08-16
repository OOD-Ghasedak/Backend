from django.db.models import F
from django.test import tag

from channels.models import Channel
from subscribe.models import Subscriber
from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestSubscribedChannels(GhasedTestCase):
    subscribed_channels_url = '/api/subscribe/joined-channels/'

    def set_up_channels(self, count):
        channels = []
        for i in range(count):
            channels.append(Channel(name=f'unit+test{i+1}'))
        Channel.objects.bulk_create(channels)

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)

    @tag('unit_api')
    def test_get_subscribed_channels(self):
        num_channels = 10
        self.set_up_channels(num_channels)
        for channel in Channel.objects.annotate(
                odd_pk=F('pk') % 2,
        ).filter(odd_pk=True):
            Subscriber.objects.create(channel=channel, ghased=self.ghased)
        data = self.client.get(
            f'{self.subscribed_channels_url}',
            HTTP_AUTHORIZATION=self.jwt_token,
            format='json',
            assert_status_code=200,
        ).json()
        for obj in data:
            self.assertTrue(obj['id'] % 2)
