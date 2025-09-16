import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedUUIDModel


class ServiceCategory(TimeStampedUUIDModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Service(TimeStampedUUIDModel):
    provider = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="services"
    )
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField(default="00:30:00")  # 30 minutes default
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="XAF")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        indexes = [
            models.Index(fields=["provider"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.provider.user.get_fullname()}"
