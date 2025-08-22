from django.contrib import admin
from .models import Payment, EscrowReleaseSchedule


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment",
        "from_user",
        "to_user",
        "amount",
        "currency",
        "payment_method",
        "status",
        "processed_at",
    )
    list_filter = ("status", "payment_method", "currency")
    search_fields = (
        "appointment__id",
        "from_user__email",
        "to_user__email",
        "external_transaction_id",
    )
    readonly_fields = ("processed_at", "released_at")


@admin.register(EscrowReleaseSchedule)
class EscrowReleaseScheduleAdmin(admin.ModelAdmin):
    list_display = ("appointment", "scheduled_release_time", "status", "processed_at")
    list_filter = ("status",)
    search_fields = ("appointment__id",)
