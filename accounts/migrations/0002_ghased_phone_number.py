# Generated by Django 3.2.4 on 2023-07-22 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ghased',
            name='phone_number',
            field=models.CharField(default='09333779699', max_length=13, unique=True, verbose_name='شماره همراه'),
            preserve_default=False,
        ),
    ]
