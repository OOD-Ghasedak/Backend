from django.test import tag

from channel_management.models import ChannelOwner, ChannelAdmin
from channels.models import Channel
from subscribe.models import Subscriber
from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestCreateUpdateContent(GhasedTestCase):
    _admins_url = None
    _admins_url_template = '/api/channels/{pk}/admins/'.format

    _subscribers_url = None
    _subscribers_url_template = '/api/channels/{pk}/subscribers/'.format

    @property
    def admins_url(self):
        return self._admins_url

    @admins_url.setter
    def admins_url(self, pk):
        self._admins_url = self._admins_url_template(pk=str(pk))

    @property
    def subscribers_url(self):
        return self._subscribers_url

    @subscribers_url.setter
    def subscribers_url(self, pk):
        self._subscribers_url = self._subscribers_url_template(pk=str(pk))

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)
        self.channel = Channel.objects.create(name='unit+test')
        self.owner = ChannelOwner.objects.create(channel=self.channel, ghased=self.ghased)
        self.admin = ChannelAdmin.objects.create(ghased=self.create_random_ghased(), channel=self.channel, share=20.5)
        self.subscriber = Subscriber.objects.create(ghased=self.create_random_ghased(), channel=self.channel)

    @tag('unit_api')
    def test_get_admins(self):
        self.admins_url = self.channel.id
        data = self.client.get(
            self.admins_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            assert_status_code=200,
        ).json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['share'], self.admin.share)
        self.assertEqual(data[0]['ghased']['username'], self.admin.ghased.user.username)
        self.assertEqual(data[0]['ghased']['email'], self.admin.ghased.email)
        self.assertEqual(data[0]['ghased']['full_name'], self.admin.ghased.user.get_full_name())

    @tag('unit_api')
    def test_get_subscribers(self):
        self.subscribers_url = self.channel.id
        data = self.client.get(
            self.subscribers_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            assert_status_code=200,
        ).json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['ghased']['username'], self.subscriber.ghased.user.username)
        self.assertEqual(data[0]['ghased']['email'], self.subscriber.ghased.email)
        self.assertEqual(data[0]['ghased']['full_name'], self.subscriber.ghased.user.get_full_name())
