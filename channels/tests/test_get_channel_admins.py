from django.test import tag

from channel_management.models import ChannelOwner, ChannelAdmin
from channels.models import Channel
from utility.tests import GhasedTestCase, APIClientCheckingDecorator


@tag('unit_test')
class TestCreateUpdateContent(GhasedTestCase):
    _admins_url = None
    _admins_url_template = '/api/channels/{pk}/admins/'.format

    @property
    def admins_url(self):
        return self._admins_url

    @admins_url.setter
    def admins_url(self, pk):
        self._admins_url = self._admins_url_template(pk=str(pk))

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)
        self.channel = Channel.objects.create(name='unit+test')
        self.owner = ChannelOwner.objects.create(channel=self.channel, ghased=self.ghased)
        ghased = self.create_random_ghased()
        self.admin = ChannelAdmin.objects.create(ghased=ghased, channel=self.channel, share=20.5)

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
