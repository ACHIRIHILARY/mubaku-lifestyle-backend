import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedUUIDModel


class ProviderAvailability(TimeStampedUUIDModel):
    provider = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="availabilities"
    )
    day_of_week = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)]
    )  # 0=Sunday, 1=Monday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Provider Availability")
        verbose_name_plural = _("Provider Availabilities")
        unique_together = ["provider", "day_of_week"]
        indexes = [
            models.Index(fields=["provider", "day_of_week"]),
        ]

    def __str__(self):
        return f"{self.provider.user.get_fullname()} - {self.get_day_of_week_display()}"


class ProviderAvailabilityException(TimeStampedUUIDModel):
    EXCEPTION_TYPES = (
        ("unavailable", _("Unavailable")),
        ("available", _("Available")),
        ("modified_hours", _("Modified Hours")),
    )

    provider = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="availability_exceptions",
    )
    exception_date = models.DateField()
    exception_type = models.CharField(max_length=20, choices=EXCEPTION_TYPES)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Provider Availability Exception")
        verbose_name_plural = _("Provider Availability Exceptions")
        unique_together = ["provider", "exception_date"]
        indexes = [
            models.Index(fields=["provider", "exception_date"]),
        ]

    def __str__(self):
        return f"{self.provider.user.get_fullname()} - {self.exception_date} ({self.get_exception_type_display()})"


class AppointmentSlot(TimeStampedUUIDModel):
    SLOT_STATUS = (
        ("available", _("Available")),
        ("booked", _("Booked")),
        ("blocked", _("Blocked")),
    )

    provider = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="slots"
    )
    slot_start = models.DateTimeField()
    slot_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=SLOT_STATUS, default="available")
    appointment = models.ForeignKey(
        "Appointment", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Appointment Slot")
        verbose_name_plural = _("Appointment Slots")
        unique_together = ["provider", "slot_start"]
        indexes = [
            models.Index(fields=["provider"]),
            models.Index(fields=["slot_start", "slot_end"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.provider.user.get_fullname()} - {self.slot_start}"


class Appointment(TimeStampedUUIDModel):
    APPOINTMENT_STATUS = (
        ("pending", _("Pending")),
        ("confirmed", _("Confirmed")),
        ("declined", _("Declined")),
        ("client_cancelled", _("Cancelled by Client")),
        ("provider_cancelled", _("Cancelled by Provider")),
        ("completed", _("Completed")),
    )

    PAYMENT_STATUS = (
        ("pending", _("Pending")),
        ("processing", _("Processing")),
        ("held_in_escrow", _("Held in Escrow")),
        ("released_to_provider", _("Released to Provider")),
        ("refunded_to_client", _("Refunded to Client")),
        ("failed", _("Failed")),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="client_appointments"
    )
    provider = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="provider_appointments"
    )
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    scheduled_for = models.DateTimeField()
    scheduled_until = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=APPOINTMENT_STATUS, default="pending"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default="XAF")
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="pending"
    )
    confirmed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
        indexes = [
            models.Index(fields=["client"]),
            models.Index(fields=["provider"]),
            models.Index(fields=["status"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["scheduled_for"]),
        ]

    def __str__(self):
        return f"{self.client.user.get_fullname()} - {self.provider.user.get_fullname()} - {self.scheduled_for}"
