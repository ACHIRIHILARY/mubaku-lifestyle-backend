from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created", "updated")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "category", "price", "currency", "is_active")
    list_filter = ("category", "is_active", "currency")
    search_fields = ("name", "provider__user__username", "category__name")
    ordering = ("name",)
