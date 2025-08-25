from django.contrib import admin
from .models import Review, Dispute


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("provider", "client", "rating", "created_at", "updated_at")
    list_filter = ("rating",)
    search_fields = ("provider__user__username", "client__user__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = (
        "appointment",
        "raised_by",
        "status",
        "resolution",
        "resolved_by",
        "resolved_at",
    )
    list_filter = ("status", "resolution")
    search_fields = ("appointment__id", "raised_by__email", "resolved_by__email")
    readonly_fields = ("resolved_at",)
