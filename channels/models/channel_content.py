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

    is_premium = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='برای کاربران اشتراکی؟',
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

    class Meta:
        verbose_name = 'محتوای کانال'
        verbose_name_plural = 'محتواهای کانال‌ها'


class ContentFile(BaseModel):

    class ContentFileTypes(Choices):
        IMAGE = Choices.Choice('image', 'تصویر')
        Video = Choices.Choice('video', 'ویدیو')
        AUDIO = Choices.Choice('audio', 'صوت')

    @staticmethod
    def content_file_upload_to(instance: 'ContentFile', filename):
        return f'channels/contents/{instance.content.channel.id}--{instance.content.id}--{filename}'

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
