# Generated by Django 3.2 on 2023-04-22 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя пользователя'),
        ),
    ]