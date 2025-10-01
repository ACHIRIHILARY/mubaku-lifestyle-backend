from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedUUIDModel


class Notification(TimeStampedUUIDModel):
    NOTIFICATION_TYPES = (
        ("appointment_reminder", _("Appointment Reminder")),
        ("payment_confirmation", _("Payment Confirmation")),
        ("booking_confirmation", _("Booking Confirmation")),
        ("review_request", _("Review Request")),
        ("promotional", _("Promotional")),
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    related_entity_type = models.CharField(max_length=50, blank=True, null=True)
    related_entity_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["is_read"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.get_fullname()}"


class LoyaltyProgram(TimeStampedUUIDModel):
    client = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="loyalty_programs"
    )
    provider = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="client_loyalty_programs",
    )
    points = models.IntegerField(default=0)
    visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Loyalty Program")
        verbose_name_plural = _("Loyalty Programs")
        unique_together = ["client", "provider"]
        indexes = [
            models.Index(fields=["client"]),
            models.Index(fields=["provider"]),
        ]

    def __str__(self):
        return f"Loyalty program: {self.client.user.get_fullname()} - {self.provider.user.get_fullname()}"
