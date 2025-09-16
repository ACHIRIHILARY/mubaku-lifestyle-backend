from django.contrib import admin
from .models import (
    ProviderAvailability,
    ProviderAvailabilityException,
    AppointmentSlot,
    Appointment,
)


@admin.register(ProviderAvailability)
class ProviderAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("provider", "day_of_week", "start_time", "end_time", "is_available")
    list_filter = ("day_of_week", "is_available")
    search_fields = ("provider__user__username",)


@admin.register(ProviderAvailabilityException)
class ProviderAvailabilityExceptionAdmin(admin.ModelAdmin):
    list_display = ("provider", "exception_date", "exception_type", "reason")
    list_filter = ("exception_type", "exception_date")
    search_fields = ("provider__user__username", "reason")


@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ("provider", "slot_start", "slot_end", "status")
    list_filter = ("status",)
    search_fields = ("provider__user__username",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "provider",
        "service",
        "scheduled_for",
        "status",
        "payment_status",
        "amount",
        "currency",
    )
    list_filter = ("status", "payment_status", "scheduled_for")
    search_fields = (
        "client__user__username",
        "provider__user__username",
        "service__name",
    )
    date_hierarchy = "scheduled_for"
