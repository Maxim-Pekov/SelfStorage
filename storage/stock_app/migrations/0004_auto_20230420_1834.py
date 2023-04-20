# Generated by Django 3.2 on 2023-04-20 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0003_storage_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Статус'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Бокс')),
                ('status', models.BooleanField(default=None, verbose_name='Статус')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('size', models.IntegerField(verbose_name='Размер')),
                ('storage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='box_storages', to='stock_app.storage', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Бокс',
                'verbose_name_plural': 'Боксы',
            },
        ),
    ]
