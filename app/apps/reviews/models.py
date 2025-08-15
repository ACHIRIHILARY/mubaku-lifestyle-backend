from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedUUIDModel


class Review(TimeStampedUUIDModel):
    appointment = models.OneToOneField(
        "appointments.Appointment", on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="reviews_given"
    )
    provider = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="reviews_received"
    )
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        indexes = [
            models.Index(fields=["provider"]),
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return f"Review for {self.provider.user.get_fullname()} by {self.client.user.get_fullname()}"


class Dispute(TimeStampedUUIDModel):
    DISPUTE_STATUS = (
        ("open", "Open"),
        ("in_review", "In Review"),
        ("resolved", "Resolved"),
    )

    DISPUTE_RESOLUTION = (
        ("payment_released", "Payment Released to Provider"),
        ("payment_refunded", "Payment Refunded to Client"),
    )

    appointment = models.OneToOneField(
        "appointments.Appointment", on_delete=models.CASCADE
    )
    raised_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="disputes_raised"
    )
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=DISPUTE_STATUS, default="open")
    admin_notes = models.TextField(blank=True, null=True)
    resolved_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="disputes_resolved",
    )
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolution = models.CharField(
        max_length=20, choices=DISPUTE_RESOLUTION, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Dispute")
        verbose_name_plural = _("Disputes")
        indexes = [
            models.Index(fields=["appointment"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Dispute for appointment #{self.appointment.id}"
