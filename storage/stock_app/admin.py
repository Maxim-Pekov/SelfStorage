from django.contrib import admin
from .models import Client, Tariff, Storage, Order, Box


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    pass


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass
