from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


class CustomUser(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=200, unique=True)
    email = models.EmailField('Почта', unique=True)
    phone = models.IntegerField('Номер телефона', null=True, blank=True)
    first_name = models.CharField('Имя', max_length=200, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=200, null=True, blank=True)


class Tariff(models.Model):
    title = models.CharField('Название тарифа', max_length=50)
    price = models.IntegerField('Цена')
    days = models.IntegerField('Количество дней')

    class Meta:
        verbose_name = 'Тариф'

    def __str__(self):
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


class BoxQuerySet(models.QuerySet):
    def calculate_box_square(self):
        return self.annotate(
            box_square=F("length") * F("width"),
        )


class Box(models.Model):
    title = models.CharField('Бокс', max_length=100)
    status = models.BooleanField('Статус', default=None)
    storage = models.ForeignKey(Storage,
                                on_delete=models.CASCADE,
                                related_name='box_storages',
                                verbose_name='Склад',
                                null=True)
    price = models.IntegerField('Цена')
    length = models.FloatField('Длина')
    width = models.FloatField('Ширина')
    height = models.FloatField('Высота')

    objects = BoxQuerySet.as_manager()

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return self.title


class Order(models.Model):
    client = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='clients',
        verbose_name='Клиент'
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
    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        related_name='boxes',
        null=True,
        verbose_name='Ячейка хранения'
    )
    paid_till = models.DateTimeField('Оплата до', null=True)
    paid_date = models.DateTimeField('Дата оплаты', null=True, default=timezone.now)

    def is_expired(self):
        return (self.paid_till - timezone.now()).days <= settings.START_RENT_REMINDER_DAYS

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f"{self.client} {self.time}"
