from functools import cached_property
from typing import Optional

from django.db import models

from utility.django import Choices
from utility.models import CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class ChannelContent(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='contents',
        verbose_name='کانال',
        on_delete=models.PROTECT,
    )

    price = models.PositiveBigIntegerField(
        verbose_name='قیمت محتوا',
        default=0,
    )

    title = models.CharField(
        max_length=256,
        verbose_name='تیتر محتوا',
        null=True, blank=True,
    )

    summary = models.TextField(
        verbose_name='خلاصه محتوا',
        null=True, blank=True,
    )

    text = models.TextField(
        verbose_name='محتوای متنی',
        null=True, blank=True,
    )

    @property
    def is_premium(self):
        return self.price > 0

    @cached_property
    def file(self) -> Optional['ContentFile']:
        return self.files.first()

    def refresh_file(self):
        try:
            del self.file
        except AttributeError:
            pass

    def refresh_from_db(self, using=None, fields=None):
        result = super().refresh_from_db(using, fields)
        self.refresh_file()
        return result

    class Meta:
        verbose_name = 'محتوای کانال'
        verbose_name_plural = 'محتواهای کانال‌ها'


def content_file_upload_to(instance: 'ContentFile', filename):
    return f'channels/contents/channel {instance.content.channel.id}, content {instance.content.id}, {filename}'


class ContentFile(BaseModel):
    class ContentFileTypes(Choices):
        IMAGE = Choices.Choice('image', 'تصویر')
        Video = Choices.Choice('video', 'ویدیو')
        AUDIO = Choices.Choice('audio', 'صوت')

        @classmethod
        def from_mime_type(cls, mime_type: str):
            type_ = mime_type.split('/')[0]
            for content_file_type in cls.get_choices():
                cft, cft_fa = content_file_type
                if type_ == cft:
                    return cft
            assert False, 'Unsupported Mime Type!'


    file = models.FileField(
        verbose_name='فایل محتوا',
        upload_to=content_file_upload_to,
    )

    file_type = models.CharField(
        choices=ContentFileTypes.get_choices(),
        max_length=64,
    )

    content = models.ForeignKey(
        to=ChannelContent,
        related_name='files',
        on_delete=models.CASCADE,
        verbose_name='کانال'
    )

    class Meta:
        verbose_name = 'فایل محتوا'
        verbose_name_plural = 'فایل‌های محتواها'
