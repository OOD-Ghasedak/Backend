# Generated by Django 3.2.4 on 2023-07-20 03:32

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('channels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, verbose_name='آیا حذف شده است؟')),
                ('channel', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='owner', to='channels.channel', verbose_name='کانال')),
                ('ghased', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='channelowner', to='accounts.ghased', verbose_name='قاصد')),
            ],
            options={
                'verbose_name': 'مالک کانال',
                'verbose_name_plural': 'مالکین کانال\u200cها',
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ChannelAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, verbose_name='آیا حذف شده است؟')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='admins', to='channels.channel', verbose_name='کانال')),
                ('ghased', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='channeladmin', to='accounts.ghased', verbose_name='قاصد')),
            ],
            options={
                'verbose_name': 'مالک کانال',
                'verbose_name_plural': 'مالکین کانال\u200cها',
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
