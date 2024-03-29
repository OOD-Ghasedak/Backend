# Generated by Django 3.2.4 on 2023-07-20 03:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ghased',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, verbose_name='آیا حذف شده است؟')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='ghased', to=settings.AUTH_USER_MODEL, verbose_name='کاربر جنگو')),
            ],
            options={
                'verbose_name': 'قاصد',
                'verbose_name_plural': 'قاصدها',
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
