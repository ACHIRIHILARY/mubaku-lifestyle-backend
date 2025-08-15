import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedUUIDModel


class Payment(TimeStampedUUIDModel):
    PAYMENT_METHODS = (
        ("mtn_momo", "MTN Mobile Money"),
        ("orange_money", "Orange Money"),
        ("card", "Credit/Debit Card"),
    )

    PAYMENT_STATUS = (
        ("initiated", "Initiated"),
        ("processing", "Processing"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("held", "Held in Escrow"),
        ("released", "Released"),
        ("refunded", "Refunded"),
    )

    appointment = models.ForeignKey(
        "appointments.Appointment", on_delete=models.CASCADE, related_name="payments"
    )
    from_user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="sent_payments"
    )
    to_user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="received_payments"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default="XAF")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_method_details = models.JSONField()  # Encrypted at application level
    external_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    escrow_release_trigger = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="initiated"
    )
    processed_at = models.DateTimeField(blank=True, null=True)
    held_until = models.DateTimeField(blank=True, null=True)
    released_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        indexes = [
            models.Index(fields=["appointment"]),
            models.Index(fields=["status"]),
            models.Index(fields=["external_transaction_id"]),
        ]

    def __str__(self):
        return f"Payment #{self.id} - {self.amount} {self.currency}"


class EscrowReleaseSchedule(TimeStampedUUIDModel):
    SCHEDULE_STATUS = (
        ("scheduled", "Scheduled"),
        ("processed", "Processed"),
        ("cancelled", "Cancelled"),
    )

    appointment = models.ForeignKey(
        "appointments.Appointment", on_delete=models.CASCADE
    )
    scheduled_release_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=SCHEDULE_STATUS, default="scheduled"
    )
    processed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Escrow Release Schedule")
        verbose_name_plural = _("Escrow Release Schedules")
        indexes = [
            models.Index(fields=["scheduled_release_time", "status"]),
        ]

    def __str__(self):
        return f"Escrow release for appointment #{self.appointment.id}"
