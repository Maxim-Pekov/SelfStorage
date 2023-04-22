from django.contrib import admin
from .models import Tariff, Storage, Order, Box, CustomUser


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


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',]
