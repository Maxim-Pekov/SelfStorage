# Generated by Django 3.2 on 2023-04-21 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0004_auto_20230420_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='size',
        ),
        migrations.AddField(
            model_name='box',
            name='height',
            field=models.FloatField(default=0, verbose_name='Высота'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='box',
            name='length',
            field=models.FloatField(default=0, verbose_name='Длина'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='box',
            name='width',
            field=models.FloatField(default=0, verbose_name='Ширина'),
            preserve_default=False,
        ),
    ]
