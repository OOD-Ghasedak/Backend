# Generated by Django 3.2.4 on 2023-08-15 08:27

from django.db import migrations, models
import utility.django


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20230803_1847'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='registerotp',
            name='email_and_phone_number_not_both_null',
        ),
        migrations.AddField(
            model_name='ghased',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='ایمیل کاربر'),
        ),
        migrations.AlterField(
            model_name='ghased',
            name='phone_number',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, validators=[utility.django.GhasedakMobileNumberValidator()], verbose_name='شماره همراه'),
        ),
        migrations.AddConstraint(
            model_name='ghased',
            constraint=models.CheckConstraint(check=models.Q(models.Q(models.Q(('email__isnull', False), models.Q(('email', ''), _negated=True)), models.Q(('phone_number__isnull', False), models.Q(('phone_number', ''), _negated=True)), _connector='OR')), name='email_and_phone_number_not_both_null_in_ghased'),
        ),
        migrations.AddConstraint(
            model_name='registerotp',
            constraint=models.CheckConstraint(check=models.Q(models.Q(models.Q(('email__isnull', False), models.Q(('email', ''), _negated=True)), models.Q(('phone_number__isnull', False), models.Q(('phone_number', ''), _negated=True)), _connector='OR')), name='email_and_phone_number_not_both_null_in_otp'),
        ),
    ]
