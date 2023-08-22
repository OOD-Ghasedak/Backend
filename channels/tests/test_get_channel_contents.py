from django.core.files import File
from django.test import tag

from channel_management.models import ChannelOwner
from channels.models import Channel, ChannelContent, ContentFile
from utility.tests import GhasedTestCase, APIClientCheckingDecorator, open_file_for_test


@tag('unit_test')
class TestGetChannelContents(GhasedTestCase):
    _contents_url = None
    _contents_url_template = '/api/channels/{pk}/contents/'.format
    _one_content_url = None
    _one_content_url_template = '/api/channels/contents/{pk}/'.format

    @property
    def contents_url(self):
        return self._contents_url

    @contents_url.setter
    def contents_url(self, pk):
        self._contents_url = self._contents_url_template(pk=str(pk))

    @property
    def one_content_url(self):
        return self._one_content_url

    @one_content_url.setter
    def one_content_url(self, pk):
        self._one_content_url = self._one_content_url_template(pk=str(pk))

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClientCheckingDecorator(self.client)
        self.channel = Channel.objects.create(name='unit+test')
        self.owner = ChannelOwner.objects.create(channel=self.channel, ghased=self.create_random_ghased())

    def get_content_from_response(self, data, id_):
        for content in data['results']:
            if str(content['id']) == str(id_):
                return content
        return None

    @tag('unit_api')
    @open_file_for_test('resources/sample.jpg')
    def test_get_contents(self):
        self.contents_url = self.channel.id
        free_content = ChannelContent.objects.create(
            channel=self.channel,
            title='first',
            summary='hello',
            text='hello world',
        )
        ContentFile.objects.create(
            content=free_content,
            file=File(self._opened_files[0]),
            file_type=ContentFile.ContentFileTypes.IMAGE,
        )
        free_content_with_no_file = ChannelContent.objects.create(
            channel=self.channel,
            title='second',
            summary='hello',
            text='hello world',
        )
        premium_content = ChannelContent.objects.create(
            channel=self.channel,
            title='third',
            summary='hello',
            text='hello world',
            price=100_000,
        )
        ContentFile.objects.create(
            content=premium_content,
            file=File(self._opened_files[0]),
            file_type=ContentFile.ContentFileTypes.IMAGE,
        )
        response = self.client.get(
            self.contents_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            format='json',
            assert_status_code=200,
        )
        data = response.json()
        self.assertIsNotNone(self.get_content_from_response(data, free_content.id)['complete_content']['file'])
        self.assertIsNotNone(self.get_content_from_response(data, free_content_with_no_file.id)['complete_content']['text'])
        self.assertIsNone(self.get_content_from_response(data, free_content_with_no_file.id)['complete_content']['file'])
        self.assertIsNone(self.get_content_from_response(data, premium_content.id)['complete_content'])

    @tag('unit_api')
    @open_file_for_test('resources/sample.jpg')
    def test_get_one_content(self):
        premium_content = ChannelContent.objects.create(
            channel=self.channel,
            title='third',
            summary='hello',
            text='hello world',
            price=100_000,
        )
        ContentFile.objects.create(
            content=premium_content,
            file=File(self._opened_files[0]),
            file_type=ContentFile.ContentFileTypes.IMAGE,
        )
        self.one_content_url = premium_content.id
        response = self.client.get(
            self.one_content_url,
            HTTP_AUTHORIZATION=self.jwt_token,
            format='json',
            assert_status_code=200,
        )
        data = response.json()
        self.assertIsNotNone(data['title'])
        self.assertIsNone(data['complete_content'])
