from modeltranslation.translator import register, TranslationOptions
from .models import Payment, EscrowReleaseSchedule


@register(Payment)
class PaymentTranslationOptions(TranslationOptions):
    fields = ("escrow_release_trigger",)


@register(EscrowReleaseSchedule)
class EscrowReleaseScheduleTranslationOptions(TranslationOptions):
    fields = ()  # only choices and verbose names, handled by gettext
