from django.test import tag

from channel_management.models import ChannelOwner
from channels.models import Channel, ChannelContent
from utility.tests import GhasedTestCase, APIClientCheckingDecorator, open_file_for_test


@tag('unit_test')
class TestCreateUpdateContent(GhasedTestCase):
    _create_contents_url = None
    _create_contents_url_template = '/api/channels/{pk}/contents/'.format
    _update_content_file_url = None
    _update_content_file_url_template = '/api/channels/contents/{pk}/'.format

    @property
    def create_contents_url(self):
        return self._create_contents_url

    @create_contents_url.setter
    def create_contents_url(self, pk):
        self._create_contents_url = self._create_contents_url_template(pk=str(pk))

    @property
    def update_content_file_url(self):
        return self._update_content_file_url

    @update_content_file_url.setter
    def update_content_file_url(self, pk):
        self._update_content_file_url = self._update_content_file_url_template(pk=str(pk))

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)
        self.channel = Channel.objects.create(name='unit+test')
        self.owner = ChannelOwner.objects.create(channel=self.channel, ghased=self.ghased)

    @tag('integrated_api')
    @open_file_for_test('resources/sample.jpg')
    def test_create_channel_with_files(self):
        self.create_contents_url = self.channel.id
        self.client.post(
            self.create_contents_url,
            data={
                'title': 'hello world',
                'price': 350_000,
                'file': self._opened_files[0]
            },
            assert_status_code=201,
            HTTP_AUTHORIZATION=self.jwt_token,
        )
        self.assertEqual(self.channel.contents.count(), 1)
        content = ChannelContent.objects.get(channel_id=self.channel.id)
        self.assertEqual(content.files.count(), 1)

        self.update_content_file_url = content.id
        self.client.patch(
            self.update_content_file_url,
            data={
                'title': 'hello worldz',
                'text': 'just a test',
                'price': 350_000,
            },
            assert_status_code=200,
            HTTP_AUTHORIZATION=self.jwt_token,
        )
        content.refresh_from_db()
        self.assertEqual(content.title, 'hello worldz')
        self.assertEqual(content.text, 'just a test')
        self.assertIsNotNone(content.file)

        self.client.patch(
            self.update_content_file_url,
            data={
                'text': 'just',
                'price': 350_000,
                'file': None,
            },
            assert_status_code=200,
            HTTP_AUTHORIZATION=self.jwt_token,
            format='json',
        )
        content.refresh_from_db()
        self.assertEqual(content.text, 'just')
        self.assertIsNone(content.file)

