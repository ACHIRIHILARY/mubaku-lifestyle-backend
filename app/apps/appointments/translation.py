from modeltranslation.translator import register, TranslationOptions
from .models import (
    ProviderAvailability,
    ProviderAvailabilityException,
    AppointmentSlot,
    Appointment,
)


@register(ProviderAvailability)
class ProviderAvailabilityTranslationOptions(TranslationOptions):
    fields = ()


@register(ProviderAvailabilityException)
class ProviderAvailabilityExceptionTranslationOptions(TranslationOptions):
    fields = ("reason",)  # Only free-text field


@register(AppointmentSlot)
class AppointmentSlotTranslationOptions(TranslationOptions):
    fields = ()


@register(Appointment)
class AppointmentTranslationOptions(TranslationOptions):
    fields = ()
