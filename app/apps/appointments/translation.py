from modeltranslation.translator import register, TranslationOptions
from .models import (
    ProviderAvailability,
    ProviderAvailabilityException,
    AppointmentSlot,
    Appointment,
)


@register(ProviderAvailability)
class ProviderAvailabilityTranslationOptions(TranslationOptions):
    # No text fields to translate (only FK, int, bool, time fields)
    fields = ()


@register(ProviderAvailabilityException)
class ProviderAvailabilityExceptionTranslationOptions(TranslationOptions):
    fields = ("reason",)  # Only free-text field


@register(AppointmentSlot)
class AppointmentSlotTranslationOptions(TranslationOptions):
    # Slot status uses choices, so you could translate via gettext in verbose_name,
    # no extra DB field translation needed.
    fields = ()


@register(Appointment)
class AppointmentTranslationOptions(TranslationOptions):
    fields = ()
