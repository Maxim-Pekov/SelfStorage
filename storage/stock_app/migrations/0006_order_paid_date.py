# Generated by Django 3.2 on 2023-04-23 06:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0005_auto_20230422_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 23, 6, 1, 22, 702165, tzinfo=utc), null=True, verbose_name='Дата оплаты'),
        ),
    ]