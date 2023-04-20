from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Client(models.Model):
    firstname = models.CharField('Имя', max_length=200)
    lastname = models.CharField('Фамилия', max_length=200, null=True, blank=True)
    phone = models.IntegerField('Номер телефона', null=True, blank=True)
    email = models.EmailField('Почта')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'  # можно грохнуть и заменить User
    

class Tariff(models.Model):
    title = models.CharField('Название тарифа', max_length=50)
    price = models.IntegerField('Цена') 
    days = models.IntegerField('Количество дней')

    class Meta:
        verbose_name = 'Тариф'

    def  __str__(self):
        return self.title


class Storage(models.Model):
    title = models.CharField('Склад', max_length=100)
    address = models.CharField('Адрес', max_length=200)
    image = models.ImageField('Фото')
    slug = models.SlugField(default='', null=False)
    status = models.BooleanField('Статус')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.address


class Box(models.Model):
    title = models.CharField('Бокс', max_length=100)
    status = models.BooleanField('Статус', default=None)
    storage = models.ForeignKey(Storage,
                                on_delete=models.CASCADE,
                                related_name='box_storages',
                                verbose_name='Склад',
                                null=True)
    price = models.IntegerField('Цена') 
    size = models.IntegerField('Размер')
    
    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return self.title


class Order(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='clients',
        verbose_name='Клиент'
    )
    address = models.CharField(
        'Адрес',
        max_length=200,
        null=True,
        blank=True
    )
    time = models.DateTimeField('Время создания заказа', auto_now=True)
    comment = models.TextField(
        'Комментарий',
        max_length=200,
        null=True,
        blank=True
    )
    tariff = models.ForeignKey(
        Tariff,
        null=True,
        on_delete=models.CASCADE,
        related_name='tariffs',
        verbose_name='Тариф'
    )
    qr_code = models.CharField(max_length=200, null=True, blank=False)
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='storages',
        null=True,
        verbose_name='Cклад'
    )
    paid_till = models.DateTimeField('Оплата до', null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return self