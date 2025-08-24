from django.contrib import admin
from .models import Notification, LoyaltyProgram


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "notification_type", "is_read", "created")
    list_filter = ("notification_type", "is_read", "created")
    search_fields = ("title", "user__email")
    ordering = ("-created",)


@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    list_display = ("client", "provider", "points", "visits", "last_visit")
    list_filter = ("visits",)
    search_fields = ("client__user__username", "provider__user__username")
